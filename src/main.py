import argparse
import logging

import cv2

from src.bounding import draw_boxes
from src.filter import mov_filter

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Simple movement based edge detection. Use the <Q> key to escape window.")
    # Add arguments
    parser.add_argument("--live", help="Pulls from a webcam if enabled.",
                        default=False, action='store_true')
    parser.add_argument("--input_file", help="Path to mp4 file to transform.",
                        default="./video/balloons.mp4")
    parser.add_argument("--frame_rate", help="Frames per second.", default=20, metavar="[1-1000]")
    parser.add_argument("--filter",
                        help="""Filters out white noise from the image. The higher the value the less gets filtered out.
                         Everything is filtered at 0, nothing is filtered at 255.""",
                        default=220, metavar="[0-255]")
    # Parse arguments
    args = parser.parse_args()
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

    last_frame = None
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        cv2.namedWindow('Transformed', cv2.WINDOW_NORMAL)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if last_frame is not None:
            transformed_frame = mov_filter(gray, last_frame, fltr)
            boxed_frame = draw_boxes(transformed_frame)

            cv2.imshow('Transformed', boxed_frame)

            if cv2.waitKey(1000 // fr) & 0xFF == ord('q'):
                break

        last_frame = gray

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
