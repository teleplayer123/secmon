import ctypes
import struct


class ELF32_Hdr(ctypes.Structure):

    _fields_ = [
        ("e_ident", ctypes.c_char*16),
        ("e_type", ctypes.c_uint16),
        ("e_machine", ctypes.c_uint16),
        ("e_version", ctypes.c_uint32),
        ("e_entry", ctypes.c_uint32),
        ("e_phoff", ctypes.c_uint32),
        ("e_shoff", ctypes.c_uint32),
        ("e_flags", ctypes.c_uint32),
        ("e_ehsize", ctypes.c_uint16),
        ("e_phentsize", ctypes.c_uint16),
        ("e_phnum", ctypes.c_uint16),
        ("e_shentsize", ctypes.c_uint16),
        ("e_shnum", ctypes.c_uint16),
        ("e_shstrndx", ctypes.c_uint16)
    ]


class ELF32:

    def __init__(self, filename):
        self.data = self._get_data(filename)
        self.elf_hdr = self._unpack_elf_hdr()
        
    def _unpack_elf_hdr(self):
        ehdr_struct = struct.Struct("16s2H5L6H")
        hdr_data = ehdr_struct.unpack(self.data[0:52])
        elf_hdr = ELF32_Hdr(*hdr_data)
        return elf_hdr

    def _get_data(self, filename):
        with open(filename, "rb") as fh:
            data = fh.read()
        return data
        

