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


class LD_R_X:
    #class for LD instructions where left operand is r
    LD_2OPS = lambda l,r: "{:02x} {:02x}".format(l, r) 
    LD_R_N = {
        "A": 0x3E,
        "B": 0x06,
        "C": 0x0E,
        "D": 0x16,
        "E": 0x1E,
        "H": 0x26,
        "L": 0x2E
    }
    
    @classmethod
    def encode_ld_r_n(self, r, n):
        op1 = self.LD_R_N.get(r.upper())
        if op1 is None:
            raise KeyError("r must be one of: A,B,C,D,E,H,L")
        ops = self.LD_2OPS(op1, n)
        return ops



