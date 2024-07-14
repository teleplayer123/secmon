import ctypes as ct
import struct

MAGIC_BYTE = 0x4D

class MPY_HDR(ct.Structure):

    _fields_ = [
        ("magic", ct.c_uint8),
        ("version", ct.c_uint8),
        ("feature_flags", ct.c_uint8),
        ("int_size", ct.c_uint8)
    ]

class MPY:

    def __init__(self, filename):
        self.data = self._get_data(filename)
        self.mpy_hdr = self.unpack_mpy_hdr()

    def unpack_mpy_hdr(self):
        hdr_struct = struct.Struct("4B")
        hdr_data = hdr_struct.unpack(self.data[0:4])
        hdr = MPY_HDR(*hdr_data)
        return hdr

    def _get_data(self, filename):
        with open(filename, "rb") as fh:
            data = fh.read()
        return data