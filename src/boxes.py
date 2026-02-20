import cv2


def merge_contours(cnts, gap=10):
    """Merge overlapping or nearby contour bounding boxes.

    cnts: list of contours
    gap: maximum gap (in pixels) between boxes to consider them adjacent

    Returns a list of boxes in (x, y, w, h) format.
    """
    # Create initial rects as (x1, y1, x2, y2)
    rects = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        rects.append((int(x), int(y), int(x + w), int(y + h)))

    if not rects:
        return []

    # Iteratively merge rects that overlap or are within `gap` pixels of each other
    merged_any = True
    while merged_any:
        merged_any = False
        new_rects = []
        used = [False] * len(rects)
        for i in range(len(rects)):
            if used[i]:
                continue
            x1, y1, x2, y2 = rects[i]
            for j in range(i + 1, len(rects)):
                if used[j]:
                    continue
                sx1, sy1, sx2, sy2 = rects[j]
                # check for overlap or proximity (within gap)
                if not (x2 < sx1 - gap or sx2 < x1 - gap or y2 < sy1 - gap or sy2 < y1 - gap):
                    # merge the two rects
                    x1 = min(x1, sx1)
                    y1 = min(y1, sy1)
                    x2 = max(x2, sx2)
                    y2 = max(y2, sy2)
                    used[j] = True
                    merged_any = True
            new_rects.append((x1, y1, x2, y2))
            used[i] = True
        rects = new_rects

    # Convert back to (x, y, w, h)
    out = [(x1, y1, x2 - x1, y2 - y1) for (x1, y1, x2, y2) in rects]
    return out
