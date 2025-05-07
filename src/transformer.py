import logging
import cv2
from src.bounding import draw_boxes

logger = logging.getLogger(__name__)

def transformer(live=False, file='./video/balloons.mp4', fr=20, fltr=220):
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
            transformed_frame = __mov_filter(gray, last_frame, fltr)
            boxed_frame = draw_boxes(transformed_frame)
            
            cv2.imshow('Transformed', boxed_frame)

            if cv2.waitKey(1000 // fr) & 0xFF == ord('q'):
                break

        last_frame = gray

    capture.release()
    cv2.destroyAllWindows()


def __mov_filter(frame, last_frame, filter):
    """
    :type filter: High pass filter that removes the most intense pixels. These pixels are usually noise.
    """
    transformed_frame = frame - last_frame
    transformed_frame[transformed_frame > filter] = 0

    return transformed_frame