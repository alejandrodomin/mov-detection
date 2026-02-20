import argparse
import logging

import cv2
from boxes import merge_contours
from tracker import Tracker

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


# `merge_contours` has been moved to `boxes.py` and is imported at module top.


# IoU helper moved to `tracker.py` which exposes Tracker class.


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

    if not live:
        logger.info(f"Starting movement detection on file {file}")
        capture = cv2.VideoCapture(file)
    else:
        capture = cv2.VideoCapture(0)

    # Create window for boxed frame
    window_name = "4. boxed"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Noise Filter", window_name, fltr, 255, lambda x: None)
    # IoU threshold (0-100 -> 0.0-1.0) and max missed frames
    cv2.createTrackbar("IoU Thresh", window_name, 30, 100, lambda x: None)
    cv2.createTrackbar("Max Missed", window_name, 5, 50, lambda x: None)

    last_frame = None
    # Tracker instance
    tracker = Tracker()

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("1. gray", gray)

        # Get current filter value from trackbars
        fltr = cv2.getTrackbarPos("Noise Filter", window_name)
        # Read IoU threshold and max missed frames from trackbars
        iou_threshold = cv2.getTrackbarPos("IoU Thresh", window_name) / 100.0
        max_missed = cv2.getTrackbarPos("Max Missed", window_name)

        # Use previous-frame differencing: wait for a previous frame
        if last_frame is None:
            last_frame = gray
            continue

        transformed_frame = cv2.absdiff(gray, last_frame)
        thresh = cv2.threshold(transformed_frame, fltr, 255, cv2.THRESH_BINARY)[1]

        boxed_frame = frame.copy()
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS
        )[0]
        boxes = merge_contours(cnts)

        # Update tracker and get current tracks
        tracks = tracker.update(boxes, iou_threshold=iou_threshold, max_missed=max_missed)

        # Draw tracks with consistent color per id
        for tid, meta in tracks.items():
            x, y, w, h = meta['bbox']
            color = (int((tid * 97) % 256), int((tid * 193) % 256), int((tid * 71) % 256))
            cv2.rectangle(boxed_frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                boxed_frame,
                str(tid),
                (x, y - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
            )
        cv2.imshow(window_name, boxed_frame)

        if cv2.waitKey(1000 // fr) & 0xFF == ord("q"):
            break

        last_frame = gray

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
