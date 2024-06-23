import ctypes as ct
import capstone as cs
import lief


MAGIC_START0 = 0x0A324655
MAGIC_START1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30

#uf2 header
class UF2_BLOCK(ct.Structure):
    
    _fields_ = [
        # 32 byte header
        ("magicStart0", ct.c_uint32),
        ("magicStart1", ct.c_uint32),
        ("flags", ct.c_uint32),
        ("targetAddr", ct.c_uint32),
        ("payloadSize", ct.c_uint32),
        ("blockNo", ct.c_uint32),
        ("numBlocks", ct.c_uint32),
        ("fileSize", ct.c_uint32), #or familyID
        # data 476 byte
        ("data", ct.c_uint8*476),
        ("magicEnd", ct.c_uint32)
    ]
