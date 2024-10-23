import struct
import ctypes as ct



class IHDR_Chunk(ct.Structure):
    """13 byte header, IHDR must be first chunk"""
    _fields_ = [
        ("width", ct.c_long),
        ("height", ct.c_long),
        ("bit_depth", ct.c_uint8),
        ("color_type", ct.c_uint8),
        ("compression", ct.c_uint8),
        ("filter", ct.c_uint8),
        ("interlace", ct.c_uint8)
    ]

class PNG:

    SIG = 0x89504E470D0A1A0A
    SIG_STRUCT = struct.Struct("B3s4B")

    def __init__(self, data):
        self.data = data

    def unpack_data(self):
        sig = self._unpack_sig()
        clen, ctype, cdata, ccrc = self._unpack_chunk(self.data[8:])
        print(f"Signature: {hex(int(sig))}")
        print("IHDR\n-------\n")
        print(f"Length: {int(clen)}")
        print(f"Type: {ctype.decode()}")
        print(f"Data: {cdata.decode()}")
        print(f"CRC: {hex(ccrc)}")

    def _unpack_sig(self):
        sig_struct = struct.Struct(">Q")
        sig = sig_struct.unpack(self.data[0:self.SIG_STRUCT.size])[0]
        return sig

    def _unpack_chunk(self, raw_chunk):
        chunk_len = int(struct.unpack(">I", raw_chunk[0:4])[0])
        print("Length: {}".format(chunk_len))
        chunk_struct = struct.Struct(">I4s{}sI".format(chunk_len))
        chunk = chunk_struct.unpack(raw_chunk[0:chunk_struct.size])
        clen = int(chunk[0])
        assert chunk_len == clen, "Unpacking Error PNG_BASE"
        chunk_type = chunk[1]
        chunk_data = chunk[2]
        chunk_crc = chunk[3] #crc32 over chunk_type and chunk_data
        return clen, chunk_type, chunk_data, chunk_crc
    
