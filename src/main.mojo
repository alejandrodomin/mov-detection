from videolib.fmp4 import Atom, uint8_to_uint32
from logger import Logger

var log = Logger()


fn main():
    try:
        with open("data/video/balloons.mp4", "r") as video:
            while True:
                bytes = video.read_bytes(4)

                if len(bytes) == 0:
                    log.info("End of file.")
                    break

                size: UInt32 = uint8_to_uint32(bytes)
                kind: String = video.read(4)
                data: List[UInt8] = video.read_bytes(Int(size) - 8)

                atom = Atom(size, kind, data)
                log.info(atom)
                if kind == "moof":
                    for a in atom.sub_atoms():
                        log.info("|->\t", a)
    except e:
        log.error("Failed with exception", e)
