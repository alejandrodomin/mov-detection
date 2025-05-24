import logging
from collections import deque

logger = logging.getLogger(__name__)


def bounding_boxes(frame):
    y_bound, x_bound = len(frame), len(frame[0])
    visited = set()
    boxes = []

    for y, row in enumerate(frame):
        for x, item in enumerate(row):
            if item > 150 and (x, y) not in visited:
                visited.add((x, y))
                queue = deque([(x, y)])

                top_left = (x_bound, y_bound)
                bot_rght = (0, 0)

                while queue:
                    coord = queue.popleft()
                    for (ii, ri) in __valid_moves(coord, (x_bound, y_bound), visited):
                        if frame[ri][ii] > 0:
                            queue.append((ii, ri))
                            visited.add((ii, ri))

                            top_left = (min(top_left[0], ii), min(top_left[1], ri))
                            bot_rght = (max(bot_rght[0], ii), max(bot_rght[1], ri))

                boxes.append((top_left, bot_rght))

    return boxes


def __valid_moves(coordinate: tuple, bounds: tuple, visited) -> list[tuple]:
    x, y = coordinate
    x_bound, y_bound = bounds

    v_moves = []
    moves = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
             (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]

    for (x, y) in moves:
        if 0 <= x < x_bound and 0 <= y < y_bound and (x, y) not in visited:
            v_moves.append((x, y))

    return v_moves

if __name__=='__main__':
    matrix = [[0, 0, 0, 0, 0],
              [0, 0, 1, 1, 0],
              [0, 0, 1, 1, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 0, 0, 1]]

    for (top_left, bottom_right) in bounding_boxes(matrix):
        print(f"Top left {top_left} bottom right {bottom_right}")