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
        ("targetAddr", ct.c_uint32), # 4 byte aligned
        ("payloadSize", ct.c_uint32), # 4 byte aligned
        ("blockNo", ct.c_uint32),
        ("numBlocks", ct.c_uint32),
        ("fileSize", ct.c_uint32), # or familyID
        # if MCU page size is more than 476 bytes, bootloader should support any payload size
        # if MCU page size is less than 476 bytes, the payload should be a multiple of page size
        ("data", ct.c_uint8*476), # data 476 bytes padded with zeros
        ("magicEnd", ct.c_uint32)
    ]

class UF2:

    def __init__(self, filename):
        self.filename = filename

    def get_flag(self, flag):
        flags = {
            "not_main_flash": 0x00000001,
            "file_container": 0x00001000,
            "family_id_present": 0x00002000,
            "md5_checksum_present": 0x00004000,
            "ext_tags_present": 0x00008000
        }

