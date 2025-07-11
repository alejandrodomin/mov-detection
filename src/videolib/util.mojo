fn uint8_to_uint32(bytes: List[UInt8]) raises -> UInt32:
    if len(bytes) != 4:
        raise Error("List does not contain 4 elements, contains", len(bytes))

    var num: UInt32 = 0
    for i in range(4):
        num = num | (UInt32(bytes[i]) << (24 - (8 * i)))

    return num
