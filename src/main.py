import argparse
import logging

import cv2

logger = logging.getLogger(__name__)


def input_parser():
    parser = argparse.ArgumentParser(
        description="Simple movement based edge detection. Use the <Q> key to escape window."
    )
    # Add arguments
    parser.add_argument(
        "--live",
        help="Pulls from a webcam if enabled.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--input_file",
        help="Path to mp4 file to transform.",
        default="./data/video/fisherman.mp4",
    )
    parser.add_argument(
        "--frame_rate", help="Frames per second.", default=20, metavar="[1-1000]"
    )
    parser.add_argument(
        "--filter",
        help="""Filters out white noise from the image. The higher the value the less gets filtered out.
                        Everything is filtered at 0, nothing is filtered at 255.""",
        default=25,
        metavar="[0-255]",
    )

    return parser


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


def main():
    logging.basicConfig(level=logging.INFO)

    # Parse arguments
    args = input_parser().parse_args()
    # Access arguments
    live = args.live
    file = args.input_file
    fr = int(args.frame_rate)
    fltr = int(args.filter)
    fr = fr if 0 < fr <= 1000 else 20

    logger.info(f"Starting movement detection on file {file}")
    if not live:
        capture = cv2.VideoCapture(file)
    else:
        capture = cv2.VideoCapture(0)

    # Create window for boxed frame
    window_name = "4. boxed"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Noise Filter", window_name, fltr, 255, lambda x: None)

    last_frame = None
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("1. gray", gray)

        if last_frame is not None:
            # Get current filter value from trackbar
            fltr = cv2.getTrackbarPos("Noise Filter", window_name)

            transformed_frame = cv2.absdiff(gray, last_frame)
            # cv2.imshow("2. transformed", transformed_frame)

            thresh = cv2.threshold(transformed_frame, fltr, 255, cv2.THRESH_BINARY)[1]
            # cv2.imshow("3. thresh", thresh)

            boxed_frame = frame.copy()
            cnts = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS
            )[0]
            boxes = merge_contours(cnts)

            for box in boxes:
                x, y, w, h = box
                cv2.rectangle(boxed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow(window_name, boxed_frame)

            if cv2.waitKey(1000 // fr) & 0xFF == ord("q"):
                break

        last_frame = gray

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
