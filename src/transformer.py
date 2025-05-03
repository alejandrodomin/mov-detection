import cv2
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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
        ax = plot_3d()

        if last_frame is not None:
            transformed_frame = __mov_filter(gray, last_frame, fltr)
            
            cv2.imshow('Transformed', transformed_frame)

            if cv2.waitKey(1000 // fr) & 0xFF == ord('q'):
                break

        last_frame = gray

    capture.release()
    cv2.destroyAllWindows()

def plot_3d():
    fig = plt.figure()
    return fig.add_subplot(111, projection='3d')


def __mov_filter(frame, last_frame, filter):
    transformed_frame = frame - last_frame
    transformed_frame[transformed_frame > filter] = 0

    return transformed_frame