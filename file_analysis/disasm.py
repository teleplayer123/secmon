import capstone as cs
import ctypes as ct
import lief
import dis
import marshal
import struct
import importlib as imp
import subprocess
import sys


def xdump(data, bs=16, en="utf8"):
    if data == "" or data is None:
        return
    width = (bs * 2) + (bs // 2)
    lines = []
    cols = """
BLOCK  BYTES{} {}\n""".format(" " * (width + (width % bs) - 5), en.upper())
    dashes = """
{0:-<6} {1:-<{2}}{3}{4}\n""".format("", "", width + (width % bs), " ","-" * (len(en)+1))
    lines.append(cols)
    lines.append(dashes)
    for i in range(0, len(data), bs):
        block_data = data[i:i+bs]
        hexstr = " ".join(["%02x" %ord(chr(x)) for x in block_data])
        txtstr = "".join(["%s" %chr(x) if 32 <= ord(chr(x)) < 127  else "." for x in block_data])
        line = "{:06x} {:48}  {:16}\n".format(i, hexstr, txtstr)
        lines.append(line)
    return "".join([i for i in lines])

def disasm_x86(filename):
    with open(filename, "rb") as fh:
        code = fh.read()
    dis = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_32)
    res = dis.disasm(code, 0x00)
    res = [ins for ins in res]
    return res
    

def disass_pyc(filename):
    with open(filename, 'rb') as f:  # Read the binary file
        magic = f.read(4)
        timestamp = f.read(4)
        code = f.read()
    try:
        # Unpack the structured content and un-marshal the code
        magic = struct.unpack('<H', magic[:2])
        timestamp = struct.unpack('<I', timestamp)
        code = marshal.loads(code)
        print(magic, timestamp, code)
    except ValueError:
        print("can't match python version")
    try:
        # Verify if the magic number corresponds with the current python version
        is_ver = struct.unpack('<H', imp.get_magic()[:2]) == magic
        print(is_ver)
    except AttributeError:
        pass
    # Disassemble the code object
    res = dis.disassemble(code)
    print(res)
    # Also disassemble that const being loaded (our function)
    res0 = dis.disassemble(code.co_consts[0])
    print(res0)
    return res, res0


#uf2 header
class UF2_BLOCK(ct.Structure):

    MAGIC_START0 = 0x0A324655
    MAGIC_START1 = 0x9E5D5157
    MAGIC_END = 0x0AB16F30
    
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


def bin_from_uf2(filename, uf2conv_path):
    outfile = str(filename.split(".")[0]) + ".bin"
    args = "{} --convert --output {}".format(filename, outfile)
    cmd = "{} {} {}".format(sys.executable, uf2conv_path, args)
    res = subprocess.call(cmd, shell=True)
    return res
    

def disasm_armv7_elf(filename):
    e_sections = {}
    elf = lief.parse(filename)
    for section in elf.sections:
        e_sections[section.name] = {
            "virtual_addr": "{:08x}".format(section.virtual_address),
            "content": section.content.hex()
        }

class DisasmElf:

    def __init__(self, filename):
        self.elf = lief.parse(filename)

    def get_libs(self):
        return self.elf.libraries

    def sections_info_dict(self):
        e_sections = {}
        for section in self.elf.sections:
            e_sections[section.name] = {
                "virtual_addr": "{:08x}".format(section.virtual_address),
                "content": section.content.hex(),
                "offset": "{:08x}".format(section.offset)
            }

    def get_imported_funcs(self):
        return [(f.name, f.value) for f in self.elf.imported_functions]
        
    def get_sec_names(self):
        return [sec.name for sec in self.elf.sections]

    def hexdump_section(self, sec_name):
        sec_content = self.elf.get_section(sec_name).content
        hex_content = xdump(sec_content)
        return hex_content