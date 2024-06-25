import ctypes
import struct
from typing import NamedTuple

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

class UF2_Data(NamedTuple):
    # if MCU page size is more than 476 bytes, bootloader should support any payload size
    # if MCU page size is less than 476 bytes, the payload should be a multiple of page size
    data: bytes # data 476 bytes padded with zeros
    magicEnd: ctypes.c_uint32

class UF2_Block(NamedTuple):
    
    uf2_hdr: UF2_Hdr
    uf2_data: UF2_Data


class UF2:

    def __init__(self, filename):
        self.data = self._get_data(filename)
        self.uf2_hdr0 = self._unpack_uf2_hdr(self.data[0:32])
        self.uf2_data0 = self._unpack_uf2_data(self.data[32:32+480])
        self.uf2_blocks = {}

    def unpack_uf2_blocks(self):
        num_blocks = len(self.data) // 512
        for i in range(num_blocks):
            curr_idx = i * 512
            hdr_idx = curr_idx + 32
            data_idx = hdr_idx + 480
            hdr = self._unpack_uf2_hdr(self.data[curr_idx:hdr_idx])
            data = self._unpack_uf2_data(self.data[hdr_idx:data_idx])
            block = UF2_Block(uf2_hdr=hdr, uf2_data=data)
            self.uf2_blocks[i] = block

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
        if end_magic != MAGIC_END:
            raise ValueError("Incorrect end block magic number: {}".format(hex(end_magic)))
        uf2_block = UF2_Data(data=data_block, magicEnd=end_magic)
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

    def __repr__(self):
        if len(self.uf2_blocks) < 1:
            raise EnvironmentError("No data to unpack")
        i = 0
        res = ""
        for idx, block in self.uf2_blocks.items():
            i += 1
            r = f"""
                Block {i}
                -----------
                magicStart0: {hex(block.uf2_hdr.magicStart0)}
                magicStart1: {hex(block.uf2_hdr.magicStart1)}
                """
            res += r
        return res