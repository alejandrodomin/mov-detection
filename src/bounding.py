import logging
from collections import deque

import numpy as np

logger = logging.getLogger(__name__)


def bounding_boxes(frame):
    step = 20
    threshold = 10

    y_bound, x_bound = len(frame), len(frame[0])
    visited = set()
    boxes = []

    for y in range(0, y_bound, step):
        for x in range(0, x_bound, step):

            if __concentration(step, (x, y), frame) > threshold and (x, y) not in visited:
                visited.add((x, y))
                queue = deque([(x, y)])

                top_left = (x_bound, y_bound)
                bot_rght = (0, 0)

                while queue:
                    coord = queue.popleft()
                    for move in __valid_moves(step, coord, (x_bound, y_bound), visited):
                        if __concentration(step, move, frame) > threshold:
                            queue.append(move)
                            visited.add(move)

                            top_left = (min(top_left[0], move[0]), min(top_left[1], move[1]))
                            bot_rght = (max(bot_rght[0], move[0]), max(bot_rght[1], move[1]))

                if top_left != (x_bound, y_bound) and bot_rght != (0, 0):
                    boxes.append((top_left, bot_rght))

    return boxes


def __valid_moves(step, coordinate: tuple, bounds: tuple, visited) -> list[tuple]:
    # TODO: implement a proximity value that would allow a certain sized casam to be considered
    #       as part of the original object
    x, y = coordinate
    x_bound, y_bound = bounds

    v_moves = []
    moves = [(x - step, y - step), (x, y - step), (x + step, y - step), (x + step, y),
             (x + step, y + step), (x, y + step), (x - step, y + step), (x - step, y)]

    for (x, y) in moves:
        if 0 <= x < x_bound and 0 <= y < y_bound and (x, y) not in visited:
            v_moves.append((x, y))

    return v_moves

def __concentration(step, coordinate, matrix):
    x, y = coordinate[0], coordinate[1]

    submatrix = matrix[y:(y + step), x:(x + step)]
    sub_sum = np.sum(submatrix)

    return sub_sum / step ** 2

if __name__=='__main__':
    matrix = [[0, 0, 0, 0, 0],
              [0, 0, 1, 1, 0],
              [0, 0, 1, 1, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 0, 0, 1]]

    for (top_left, bottom_right) in bounding_boxes(matrix):
        print(f"Top left {top_left} bottom right {bottom_right}")