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