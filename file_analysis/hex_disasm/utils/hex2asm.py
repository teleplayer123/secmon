from capstone import *
import sys

from headers.intel_hex_file import IntelHexFile


def dis_intel_hex(fname):
    xfile = IntelHexFile(fname)
    code = xfile.records
    return code

def cap_dis_hex(fname):
    disasm = Cs(CS_ARCH_X86, CS_MODE_64)
    with open(fname, "r") as fh:
        code = fh.read()
    res = disasm.disasm(code, offset=0x0000)
    return res