from videolib.fmp4 import Video
from videolib.util import uint8_to_uint32

from logger import Logger

var log = Logger()


fn main():
    try:
        var balloons = Video("data/video/balloons.mp4")

        balloons.frames()
    except e:
        log.error("Failed with exception", e)
