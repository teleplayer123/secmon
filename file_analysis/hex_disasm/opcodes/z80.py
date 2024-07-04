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
    """class for LD instructions where left operand is r"""

    LD_R_N = lambda r, n: "{:02x} {:02x}".format(int(f"0b00{r}110", 2), n) 
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
    def encode_ld_r_n(self, r, n):
        op1 = self.LD_R.get(r.upper())
        if op1 is None:
            raise KeyError("r must be one of: A,B,C,D,E,H,L")
        ops = self.LD_R_N(op1, n)
        return ops

