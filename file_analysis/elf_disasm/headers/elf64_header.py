import ctypes
import struct


class ELF64_Hdr(ctypes.Structure):

    _fields_ = [
        ("e_ident", ctypes.c_char*16),
        ("e_type", ctypes.c_uint16),
        ("e_machine", ctypes.c_uint16),
        ("e_version", ctypes.c_uint32),
        ("e_entry", ctypes.c_uint64),
        ("e_phoff", ctypes.c_uint64),
        ("e_shoff", ctypes.c_uint64),
        ("e_flags", ctypes.c_uint32),
        ("e_ehsize", ctypes.c_uint16),
        ("e_phentsize", ctypes.c_uint16),
        ("e_phnum", ctypes.c_uint16),
        ("e_shentsize", ctypes.c_uint16),
        ("e_shnum", ctypes.c_uint16),
        ("e_shstrndx", ctypes.c_uint16)
    ]


class ELF64:

    def __init__(self, filename):
        self.data = self._get_data(filename)
        self.elf_hdr = self._unpack_elf_hdr()
        
    def _unpack_elf_hdr(self):
        pass

    def _get_data(self, filename):
        with open(filename, "rb") as fh:
            data = fh.read()
        return data