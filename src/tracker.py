"""Simple IoU-based tracker with Hungarian matching fallback to greedy.

Tracks are stored as a dict: id -> {'bbox': (x,y,w,h), 'missed': int}
"""
from typing import List, Tuple


def _iou(boxA: Tuple[int, int, int, int], boxB: Tuple[int, int, int, int]) -> float:
    xA1, yA1, wA, hA = boxA
    xA2, yA2 = xA1 + wA, yA1 + hA
    xB1, yB1, wB, hB = boxB
    xB2, yB2 = xB1 + wB, yB1 + hB

    xi1 = max(xA1, xB1)
    yi1 = max(yA1, yB1)
    xi2 = min(xA2, xB2)
    yi2 = min(yA2, yB2)
    inter_w = max(0, xi2 - xi1)
    inter_h = max(0, yi2 - yi1)
    inter = inter_w * inter_h
    areaA = wA * hA
    areaB = wB * hB
    union = areaA + areaB - inter
    return inter / union if union > 0 else 0.0


class Tracker:
    def __init__(self, iou_threshold: float = 0.3, max_missed: int = 5):
        self.tracks = {}  # id -> {'bbox': (x,y,w,h), 'missed': int}
        self._next_id = 0
        self.iou_threshold = iou_threshold
        self.max_missed = max_missed

    def update(self, boxes: List[Tuple[int, int, int, int]], iou_threshold=None, max_missed=None):
        """Update tracker with newly detected boxes.

        boxes: list of (x,y,w,h)
        Returns: current tracks dict
        """
        if iou_threshold is None:
            iou_threshold = self.iou_threshold
        if max_missed is None:
            max_missed = self.max_missed

        track_ids = list(self.tracks.keys())
        unmatched_tracks = set(track_ids)
        unmatched_boxes = set(range(len(boxes)))

        # Build IoU matrix
        iou_matrix = []
        for tid in track_ids:
            row = []
            for b in boxes:
                row.append(_iou(self.tracks[tid]['bbox'], b))
            iou_matrix.append(row)

        matched = {}
        if iou_matrix:
            try:
                # Prefer Hungarian
                from scipy.optimize import linear_sum_assignment
                import numpy as np

                cost_matrix = 1.0 - np.array(iou_matrix)
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                for r, c in zip(row_ind, col_ind):
                    if r < len(track_ids) and c < len(boxes):
                        iou_val = iou_matrix[r][c]
                        if iou_val >= iou_threshold:
                            tid = track_ids[r]
                            matched[tid] = c
                            unmatched_tracks.discard(tid)
                            unmatched_boxes.discard(c)
            except Exception:
                # Fallback greedy
                import heapq

                heap = []
                for t_idx, tid in enumerate(track_ids):
                    for b_idx in range(len(boxes)):
                        heap.append((-iou_matrix[t_idx][b_idx], t_idx, b_idx))
                heapq.heapify(heap)
                used_t = set()
                used_b = set()
                while heap:
                    neg_iou, t_idx, b_idx = heapq.heappop(heap)
                    iou_val = -neg_iou
                    if iou_val < iou_threshold:
                        break
                    if t_idx in used_t or b_idx in used_b:
                        continue
                    tid = track_ids[t_idx]
                    matched[tid] = b_idx
                    used_t.add(t_idx)
                    used_b.add(b_idx)
                    unmatched_tracks.discard(tid)
                    unmatched_boxes.discard(b_idx)

        # Update matched tracks
        for tid, b_idx in matched.items():
            self.tracks[tid]['bbox'] = boxes[b_idx]
            self.tracks[tid]['missed'] = 0

        # Create new tracks
        for b_idx in sorted(unmatched_boxes):
            self.tracks[self._next_id] = {'bbox': boxes[b_idx], 'missed': 0}
            self._next_id += 1

        # Increase missed count for unmatched tracks and remove stale ones
        to_delete = []
        for tid in unmatched_tracks:
            self.tracks[tid]['missed'] += 1
            if self.tracks[tid]['missed'] > max_missed:
                to_delete.append(tid)
        for tid in to_delete:
            del self.tracks[tid]

        return self.tracks
