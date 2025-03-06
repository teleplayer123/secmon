from typing import NamedTuple


class MagicValues:
    """
    Magic file signatures
    Tuple format: (hex_value, offset)
    Assumes little endian
    """
    PDF = ("\x25\x50\x44\x46\x2D", 0)
    PCAP = ("\xD4\xC3\xB2\xA1", 0)
    PCAPNG = ("\x0A\x0D\x0D\x0A", 0)
    SQLLITE = ("\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33\x00", 0)
    BZ2 = ("\x42\x5A\x68", 0)
    GIF1 = ("\x47\x49\x46\x38\x37\x61", 0)
    GIF2 = ("\x47\x49\x46\x38\x39\x61", 0)
    ICO = ("\x00\x00\x01\x00", 0) # computer icon encoded in ICO file format
    ICNS = ("\x69\x63\x6e\x73", 0) # apple icon image format
    BZ2 = ("\x42\x5A\x68", 0) # bzip2 compressiom 
    TIF = ("\x49\x49\x2A\x00", 0) # tagged image file format (TIFF)
    BGP = ("\x42\x50\x47\xFB", 0) # better portable graphics format
    EXR = ("\x76\x2F\x31\x01", 0) # openEXR image
    JPG = ("\xFF\xD8\xFF\xDB", 0) # jpeg raw or in JFIF or Exif format
    JPEG = ("\xFF\xD8\xFF\xE0", 0) # jpeg raw or in JFIF or Exif format
    PNG = ("\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", 0) # portable network graphics format
    H5 = ("\x89\x48\x44\x46\x0D\x0A\x1A\x0A", [0, 512, 1024, 2048]) # hierarchical data format version 5 (HDF5)
    CHM = ("\x49\x54\x53\x46\x03\x00\x00\x00\x60\x00\x00\x00", 0) # MS Windows HtmlHelp Data
    OGG = ("\x4F\x67\x67\x53", 0) # ogg open source media container format
    PSD = ("\x38\x42\x50\x53", 0) # adobe phtotoshop native file format
    WAV = ("\x52\x49\x46\x46\x00\x00\x00\x00\x57\x41\x56\x45", 0) # wav audio file format
    AVI = ("\x52\x49\x46\x46\x00\x00\x00\x00\x41\x56\x49\x20", 0) # audio video interleave video format
    MP3 = ("\x49\x44\x33", 0) # mp3 file format with ID3v2 container
    BMP = ("\x42\x4D", 0) # bitmap format mostly used in windows
    ISO = ("\x43\x44\x30\x30\x31", [0x8001, 0x8801, 0x9001]) # ISO9660 CD/DVD image file
    

    @staticmethod
    def x2a(vals):
        """convert raw hex string to ascii"""
        return "".join([v for v in vals])
    
    @staticmethod
    def x2i(vals):
        """convert raw hex string to space separated hex string format 0xXX"""
        return " ".join([hex(ord(v)) for v in vals])


MAGIC_NUMS = {
    "PDF": {
        "hex": "\x25\x50\x44\x46\x2D",
        "ascii": "%PDF-",
        "offset": 0
    },
    "PCAP": {
        "hex": "\xD4\xC3\xB2\xA1",
        "ascii": f"{chr(0xD4)}{chr(0xC3)}{chr(0xB2)}{chr(0xA1)}",
        "offset": 0
    }
}