import ctypes as ct
import struct


"""
0 1:    Zeros (0) and ones (1) mean binary 0 and 1.
i:      Lower case “i” denotes a bit that is affected by immediate status.
d s:    Lower case “d” and “s” indicate destination and source bits.
?:      Question marks denote bits that are dynamically set by the compiler.
---:    Hyphens indicate items that are not applicable or not important.
..:     Double-periods represent a range of contiguous values.

common syntax elements
-----------------------
[Label] [Condition] <Instruction> <Operands> [Effects]

- Label: an optional statement label. Label can be global (starting with an underscore
'_' or a letter) or can be local (starting with a colon ':'). Local Labels must be
separated from other same-named local labels by at least one global label. Label is
used by instructions like JMP, CALL and COGINIT to designate the target destination.
See Global and Local Labels on page 242 for more information.
- Condition: an optional execution condition (IF_C, IF_Z, etc.) that causes Instruction
to be executed or not. See IF_x (Conditions) on page 295 for more information.
- Instruction and Operands: a Propeller Assembly instruction (MOV, ADD, COGINIT, etc.)
and its zero, one, or two operands as required by the Instruction.
- Effects: an optional list of one to three execution effects (WZ, WC, WR, and NR) to apply
to the instruction, if executed. They cause the Instruction to modify the Z flag, C 

opcode fields:
--------------
INSTR (bits 31:26) - Indicates the instruction being executed.
ZCRI (bits 25:22) - Indicates instruction's effect status and SRC field meaning.
CON (bits 21:18) - Indicates the condition in which to execute the instruction.
DEST (bits 17:9) - Contains the destination register address.
SRC (bits 8:0) - Contains the source register address or 9-bit literal value. 
*The Z and C bits of the ZCRI field are clear (0) by default and are set (1) if the instruction was specified with a WZ and/or WC effect.
"""

#assembly reference
#Instruction    INSTR   ZCRI  CON DEST SRC   Z-Result   C-Result        Result      Clocks
#-------------------------------------------------------------------------------------------
ABS =           "101010 001{} 1111 {} {}"  # result=0   S[31]           written     4                 
ABSNEG =        "101011 001{} 1111 {} {}"  # result=0   S[31]           written     4         
ADD =           "100000 001{} 1111 {} {}"  # D+S=0      unsigned carry  written     4

