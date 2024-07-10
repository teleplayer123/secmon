from typing import NamedTuple


"""
OPCode Symbols:
    r: Identifies any of the registers A, B, C, D, E, H, or L
    (HL): Identifies the contents of the memory location, whose address is specified by the contents of the register pair HL
    (IX+d): Identifies the contents of the memory location, whose address is specified by the contents of the Index register pair IX plus the signed displacement d
    (IY+d): Identifies the contents of the memory location, whose address is specified by the contents of the Index register pair IY plus the signed displacement d
    n: Identifies a one-byte unsigned integer expression in the range (0 to 255)
    nn: Identifies a two-byte unsigned integer expression in the range (0 to 65535)
    d: Identifies a one-byte signed integer expression in the range (-128 to +127)
    b: Identifies a one-bit expression in the range (0 to 7). The most-significant bit to the left is bit 7 and the least-significant bit to the right is bit 0
    e: Identifies a one-byte signed integer expression in the range (-126 to +129) for relative jump offset from current location
    cc: Identifies the status of the Flag Register as any of (NZ, Z, NC, C, PO, PE, P, or M) for the conditional jumps, calls, and return instructions
    qq: Identifies any of the register pairs BC, DE, HL or AF
    ss: Identifies any of the register pairs BC, DE, HL or SP
    pp: Identifies any of the register pairs BC, DE, IX or SP
    rr: Identifies any of the register pairs BC, DE, IY or SP
    s: Identifies any of r, n, (HL), (IX+d) or (IY+d)
    m: Identifies any of r, (HL), (IX+d) or (IY+d)
"""

class LD_R_KeyError(Exception):
    def __init__(self):
        self.message = "r must be one of: A,B,C,D,E,H,L"
        super().__init__(self.message)

class LD_8Bit:
    """class for LD instructions"""

    LD_R_R = lambda r0, r1: "{:02x}".format(int(f"0b01{r0}{r1}", 2))
    LD_R_N = lambda r, n: "{:02x} {:02x}".format(int(f"0b00{r}110", 2), n) 
    LD_R_HL = lambda r: "{:02x}".format(int(f"0b01{r}110", 2))
    LD_R_IX_D = lambda r, d: "{:02x} {:02x} {:02x}".format(int("0b11011101", 2), int(f"0b01{r}110", 2), d)
    LD_R_IY_D = lambda r, d: "{:02x} {:02x} {:02x}".format(int("0b11111101", 2), int(f"0b01{r}110", 2), d)
    LD_HL_R = lambda r: "{:02x}".format(int(f"0b01110{r}", 2))
    LD_IX_D_R = lambda r, d: "{:02x} {:02x} {:02x}".format(int("0b11011101", 2), int(f"0b01110{r}", 2), d)
    LD_IY_D_R = lambda r, d: "{:02x} {:02x} {:02x}".format(int("0b11111101", 2), int(f"0b01110{r}", 2), d)
    LD_HL_N = lambda n: "{:02x} {:02x}".format(int("0b00110110", 2), n)
    LD_IX_D_N = lambda d, n: "{:02x} {:02x} {:02x} {:02x}".format(int("0b11011101", 2), int("0b00110110", 2), d, n)
    LD_IY_D_N = lambda d, n: "{:02x} {:02x} {:02x} {:02x}".format(int("0b11111101", 2), int("0b00110110", 2), d, n)
    LD_A_BC = "0A"
    LD_A_DE = "1A"
    LD_BC_A = "02"
    LD_DE_A = "12"
    LD_I_A = "ED 47"
    LD_R_A = "ED 4F"
    LD_A_I = "ED 57"  #condition bits are affected
    LD_A_R = "ED 5F"  #condition bits are affected
    LD_NN_A = lambda n0, n1: "{:02x} {:02x} {:02x}".format(int("0b00110010", 2), n0, n1)
    LD_A_NN = lambda n0, n1: "{:02x} {:02x} {:02x}".format(int("0b00111010", 2), n0, n1)
    LD_R = {
        "A": "111",
        "B": "000",
        "C": "001",
        "D": "010",
        "E": "011",
        "H": "100",
        "L": "101"
    }

    @classmethod
    def encode_ld_r_r(self, r0, r1):
        op1 = self.LD_R.get(r0)
        op2 = self.LD_R.get(r1)
        if op1 is None or op2 is None:
            raise LD_R_KeyError()
        ops = self.LD_R_R(op1, op2)
        return ops
    
    @classmethod
    def encode_ld_r_n(self, r, n):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        ops = self.LD_R_N(op1, n)
        return ops

    @classmethod
    def encode_ld_r_hl(self, r):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        op = self.LD_R_HL(op1)
        return op
    
    @classmethod
    def encode_ld_r_ix_d(self, r, d):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        ops = self.LD_R_IX_D(op1, d)
        return ops

    @classmethod
    def encode_ld_r_iy_d(self, r, d):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        ops = self.LD_R_IY_D(op1, d)
        return ops
    
    @classmethod
    def encode_ld_hl_r(self, r):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        op = self.LD_HL_R(op1)
        return op

    @classmethod
    def encode_ld_ix_d_r(self, d, r):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        ops = self.LD_IX_D_R(op1, d)
        return ops

    @classmethod
    def encode_ld_iy_d_r(self, d, r):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise LD_R_KeyError()
        ops = self.LD_IY_D_R(op1, d)
        return ops

    @classmethod
    def encode_ld_hl_n(self, n):
        ops = self.LD_HL_N(n)
        return ops

    @classmethod
    def encode_ld_ix_d_n(self, d, n):
        ops = self.LD_IX_D_N(d, n)
        return ops
    
    @classmethod
    def encode_ld_iy_d_n(self, d, n):
        ops = self.LD_IY_D_N(d, n)
        return ops

