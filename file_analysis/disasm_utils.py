import capstone as cs
import ctypes as ct
import lief


def disasm_x86(filename):
    with open(filename, "rb") as fh:
        code = fh.read()
    dis = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_32)
    res = dis.disasm(code, 0x00)
    res = [ins for ins in res]
    return res

def disasm_arm(filename):
    with open(filename, "rb") as fh:
        code = fh.read()
    dis = cs.Cs(cs.CS_ARCH_ARM, cs.CS_MODE_ARM)
    res = dis.disasm(code, 0x00)
    res = [ins for ins in res]
    return res


class BinDisasm:

    def __init__(self, filename, arch, mode, size=None):
        self.filename = filename
        self._size = size
        self._data_fd = None
        self.data = None
        self._code = None
        self._arch = arch
        self._mode = mode
        self._dis = None
        
    def _get_code(self, offset=0):
        self._dis = cs.Cs(self._arch, self._mode)
        code = self._dis.disasm(self.data, offset=offset)
        return [ins for ins in code]
    
    def reconfig_mode(self, mode):
        if self._dis is not None:
            self._dis.mode = mode
        else:
            raise EnvironmentError("File must be parsed before reconfiguring mode.")
        
    def set_syntax(self, syntax):
        if self._dis is not None:
            self._dis.syntax = syntax
        else:
            raise EnvironmentError("File must be parsed before setting syntax format.")

    def parse_code(self, offset=0):
        ins_info = {}
        code = self._get_code(offset)
        for i in code:
            ins_by_addr = {
                "address": i.address,
                "mnemonic": i.mnemonic,
                "operation": i.op_str
            }
        return ins_info

    def __enter__(self):
        self._data_fd = open(self.filename, "rb")
        if self._size is not None and type(self._size) == int:
            self.data = self._data_fd.read(self._size)
        else:
            self.data = self._data_fd.read()
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._data_fd.close()