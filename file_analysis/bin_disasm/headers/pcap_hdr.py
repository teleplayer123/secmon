import ctypes as ct
import struct


MAGIC_NUM_MICRO = 0xA1B2C3D4 
MAGIC_NUM_NANO = 0xA1B23C4D

class PCAP_HDR(ct.Structure):

    _fields_ = [
        ("magic_number", ct.c_uint32),
        ("version_major", ct.c_uint16),
        ("version_minor", ct.c_uint16),
        ("thiszone", ct.c_uint32),
        ("sigfigs", ct.c_uint32),
        ("snaplen", ct.c_uint32),
        ("network", ct.c_uint32)
    ]

class PCAP_REC(ct.Structure):

    _fields_ = [
        ("ts_sec", ct.c_uint32),
        ("ts_usec", ct.c_uint32),
        ("incl_len", ct.c_uint32),
        ("orig_len", ct.c_uint32)
    ]

class PCAPHeader:
    
    HDR_STRUCT = struct.Struct("LHHLLLL")

    def __init__(self, raw_data, create=False):
        if create == False:
            self.data = self.HDR_STRUCT.unpack(raw_data)
        else:
            self.data = self.HDR_STRUCT.pack(raw_data)


class PacketRecord:

    PKT_STRUCT = struct.Struct("LLLL")

    def __init__(self, raw_data, create=False):
        if create == False:
            self.data = self.PKT_STRUCT.unpack(raw_data)
        else:
            self.data = self.PKT_STRUCT.pack(raw_data)
