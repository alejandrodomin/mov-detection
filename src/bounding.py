def draw_boxes(frame: list[list[int]], box_size: int = 8, threshold: int = 25):
    for box in __boxes(frame, box_size, threshold):
        top_left, bottom_right = box

        for row in range(top_left[0], bottom_right[0]):
            frame[row][top_left[1]] = 255
            frame[row][bottom_right[1]] = 255

        for column in range(top_left[1], bottom_right[1]):
            frame[top_left[0]][column] = 255
            frame[bottom_right[1]][column] = 255

    return frame

def __boxes(frame, box_size, threshold) -> list[tuple]:
    boxes_arr = []

    for i in range(0, len(frame) - box_size, box_size):
        for j in range(0, len(frame[i]) - box_size, box_size):
            box = __box_builder(box_size, frame, i, j)

            box_sum = sum([sum(row) for row in box]) / box_size ** 2
            if box_sum > threshold:
                boxes_arr.append([(i, j), (i + box_size, j + box_size)])

    return __merge_boxes(boxes_arr)


def __box_builder(box_size, frame, row_index, item_index):
    box = []
    for i in range(box_size):
        box_row = []
        for j in range(box_size):
            box_row.append(frame[row_index + i][item_index + j])

        box.append(box_row)
    return box


def __merge_boxes(boxes: list[tuple]) -> list[tuple]:
    done = False
    while not done:
        box = boxes.pop()

        for other_box in boxes:
            if __overlap(box, other_box):
                boxes.remove(other_box)

                top_left = (min(box[0][0], other_box[0][0]), min(box[0][1], other_box[0][1]))
                bottom_right = (max(box[1][0], other_box[1][0]), max(box[1][1], other_box[1][1]))

                boxes.append((top_left, bottom_right))
                break

    return boxes


def __overlap(box, other_box):
    top_left_box, bottom_right_box = box
    top_left_other, bottom_right_other = other_box

    # TODO: I know there needs to be more check here. But I don't feel like thinking about it now.
    return top_left_box[0] <= top_left_other[0] <= bottom_right_other[0] or top_left_box[1] <= top_left_other[1] <= \
        bottom_right_other[1]