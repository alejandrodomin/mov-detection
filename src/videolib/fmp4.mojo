from videolib.util import uint8_to_uint32
from logger import Logger

var log = Logger()


struct Video:
    var atoms: List[Atom]

    fn __init__(out self, atoms: List[Atom]):
        self.atoms = atoms

    fn __init__(out self, path: String) raises:
        self.atoms = []

        with open(path, "r") as video:
            while True:
                sizeBytes = video.read_bytes(4)

                if len(sizeBytes) == 0:
                    log.debug("Finished processing mp4.")
                    break

                size: UInt32 = uint8_to_uint32(sizeBytes)
                kind: String = video.read(4)
                data: List[UInt8] = video.read_bytes(Int(size) - 8)

                self.atoms.append(Atom(size, kind, data))


struct Atom(Stringable, Writable, Copyable, Movable):
    """Breakdown of the atom types within a fragmented MP4 formatted file.
        [ftyp][moov][moof][mdat][moof][mdat]...(repeat [moof][mdat]).

        |ftyp
        |moov: - contains video track and codec info
        |    - trak
        |    - mdia
        |    - tsd
        |    - avc1
        |moof:
        |    - traf:
        |        - tfhd: track fragment header
        |        - trun: information about sample count, size, duration, and offset
        |                   information used to know where the samples are in mdat
        |mdat:
        |    - trun - contains raw media data
    ."""

    var size: UInt32
    var kind: String
    var data: List[UInt8]
    var subAtoms: List[Atom]

    fn __init__(out self, size: UInt32, kind: String, data: List[UInt8]) raises:
        self.size = size
        self.kind = kind
        self.data = data
        self.subAtoms = []

        if self.__has_children(self.kind):
            self.subAtoms = self.__sub_atoms()

    fn __moveinit__(out self, owned existing: Self):
        self.size = existing.size
        self.kind = existing.kind
        self.data = existing.data
        self.subAtoms = existing.subAtoms

    fn __str__(self) -> String:
        subAtomStr: String = ""
        for atom in self.subAtoms:
            subAtomStr = subAtomStr + String(atom) + "\n"

        return (
            "Atom: "
            + self.kind
            + " of size "
            + String(self.size)
            + "\n"
            + subAtomStr
        )

    fn write_to[W: Writer](self, mut writer: W):
        writer.write(String(self))

    fn __sub_atoms(self) raises -> List[Atom]:
        atoms: List[Atom] = []

        index: Int = 0
        while index < len(self.data):
            size: UInt32 = uint8_to_uint32(self.data[index : index + 4])

            kind: String = ""
            for byte in self.data[index + 4 : index + 8]:
                kind = kind + chr(Int(byte))

            data: List[UInt8] = self.data[index + 8 : index + Int(size)]

            atoms.append(Atom(size, kind, data))

            index += Int(size)

        return atoms

    fn __has_children(self, kind: String) -> Bool:
        var kinds: List[String] = ["moov", "moof", "traf"]

        return kind in kinds
