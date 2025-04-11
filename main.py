import cv2
import argparse

import pdb

def transformer(live=False, file='./video/balloons.mp4', fr=20, fltr=220):
    if not live:
        capture = cv2.VideoCapture(file)
    else:
        capture = cv2.VideoCapture(0)

    lastFrame=None
    while capture.isOpened():
        ret, frame = capture.read()
        
        if not ret:
            break
   
        cv2.namedWindow('Transformed', cv2.WINDOW_NORMAL)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if lastFrame is not None:
            trnsfrmdFrame = gray - lastFrame

            trnsfrmdFrame[trnsfrmdFrame > fltr] = 0

            cv2.imshow('Transformed', trnsfrmdFrame)
    
            if cv2.waitKey(1000//fr) & 0xFF == ord('q'):
                break 

        lastFrame=gray

    capture.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Simple movement based edge detection. Use the <Q> key to escape window.")

    # Add arguments
    parser.add_argument("--live", help="Pulls from a webcam if enabled.", default=False, action='store_true')
    parser.add_argument("--input_file", help="Path to mp4 file to transform.", default="./video/balloons.mp4")
    parser.add_argument("--frame_rate", help="Frames per second.", default=20, metavar="[1-1000]")
    parser.add_argument("--filter", help="Filters out white noise from the image. The higher the value the less gets filtered out. Everything is filtered at 0, nothing is filtered at 255.", default=220, metavar="[0-255]")

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    live=args.live
    file=args.input_file
    fr=int(args.frame_rate)
    fltr=int(args.filter)

    fr=fr if fr > 0 and fr <= 1000 else 20

    transformer(live, file, fr, fltr)
