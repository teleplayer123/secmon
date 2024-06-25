import ctypes
import struct


MAGIC_START0 = 0x0A324655
MAGIC_START1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30

#uf2 512 byte block
class UF2_Hdr(ctypes.Structure):
    
    _fields_ = [
        # 32 byte header
        ("magicStart0", ctypes.c_uint32),
        ("magicStart1", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("targetAddr", ctypes.c_uint32), # 4 byte aligned
        ("payloadSize", ctypes.c_uint32), # 4 byte aligned
        ("blockNo", ctypes.c_uint32),
        ("numBlocks", ctypes.c_uint32),
        ("fileSize", ctypes.c_uint32), # or familyID
    ]

class UF2_Data(ctypes.Structure):
    _fields_ = [
        # if MCU page size is more than 476 bytes, bootloader should support any payload size
        # if MCU page size is less than 476 bytes, the payload should be a multiple of page size
        ("data", ctypes.c_char_p), # data 476 bytes padded with zeros
        ("magicEnd", ctypes.c_uint32)
    ]

class UF2:

    def __init__(self, filename):
        self.data = self._get_data(filename)
        self.uf2_hdr0 = self._unpack_uf2_hdr(self.data[0:32])
        self.uf2_data0 = self._unpack_uf2_data(self.data[32:32+480])

    def _unpack_uf2_hdr(self, data):
        uf2_struct = struct.Struct("8L")
        uf2_hdr = uf2_struct.unpack(data)
        uf2_hdr_block = UF2_Hdr(*uf2_hdr)
        return uf2_hdr_block
    
    def _unpack_uf2_data(self, data):
        data_struct = struct.Struct("476s")
        end_struct = struct.Struct("L")
        data_block = data_struct.unpack(data[:476])[0]
        end_magic = end_struct.unpack(data[476:480])[0]
        uf2_block = UF2_Data()
        uf2_block.data = data_block
        if end_magic != MAGIC_END:
            raise ValueError("Incorrect end block magic number: {}".format(hex(end_magic)))
        uf2_block.magicEnd = end_magic
        return uf2_block

    def _get_data(self, filename):
        with open(filename, "rb") as fh:
            data = fh.read()
        return data

    def get_flag(self, flag):
        flags = {
            "not_main_flash": 0x00000001,
            "file_container": 0x00001000,
            "family_id_present": 0x00002000,
            "md5_checksum_present": 0x00004000,
            "ext_tags_present": 0x00008000
        }

