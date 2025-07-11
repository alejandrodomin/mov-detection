struct Atom(Stringable, Writable, Copyable, Movable):
    var size: UInt32
    var kind: String
    var data: List[UInt8]

    fn __init__(out self, size: UInt32, kind: String, data: List[UInt8]):
        self.size = size
        self.kind = kind
        self.data = data

    fn __moveinit__(out self, owned existing: Self):
        self.size = existing.size
        self.kind = existing.kind
        self.data = existing.data

    fn __str__(self) -> String:
        return "Atom: " + self.kind + " of size " + String(self.size)

    fn write_to[W: Writer](self, mut writer: W):
        writer.write(String(self))

    fn sub_atoms(self) raises -> List[Atom]:
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


fn uint8_to_uint32(bytes: List[UInt8]) raises -> UInt32:
    if len(bytes) != 4:
        raise Error("List is wrong size to convert.", len(bytes))

    var num: UInt32 = 0
    for i in range(4):
        num = num | (UInt32(bytes[i]) << (24 - (8 * i)))

    return num
