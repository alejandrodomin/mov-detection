import argparse
import logging

from src.transformer import transformer

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.NOTSET)

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
    transformer(live, file, fr, fltr)


if __name__ == '__main__':
    main()
