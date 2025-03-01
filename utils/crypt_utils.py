from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
import base64


CHAR_FREQ_DICT = {
    "a": 8.2,
    "b": 1.5,
    "c": 2.8,
    "d": 4.3,
    "e": 13.0,
    "f": 2.2,
    "g": 2.0,
    "h": 6.1,
    "i": 7.0,
    "j": 0.15,
    "k": 0.77,
    "l": 4.0,
    "m": 2.4,
    "n": 6.7,
    "o": 7.5,
    "p": 1.9,
    "q": 0.095,
    "r": 6.0,
    "s": 6.3,
    "t": 9.1,
    "u": 2.8,
    "v": 0.98,
    "w": 2.4,
    "x": 0.15,
    "y": 2.0,
    "z": 0.074,
    "A": 8.2,
    "B": 1.5,
    "C": 2.8,
    "D": 4.3,
    "E": 13.0,
    "F": 2.2,
    "G": 2.0,
    "H": 6.1,
    "I": 7.0,
    "J": 0.15,
    "K": 0.77,
    "L": 4.0,
    "M": 2.4,
    "N": 6.7,
    "O": 7.5,
    "P": 1.9,
    "Q": 0.095,
    "R": 6.0,
    "S": 6.3,
    "T": 9.1,
    "U": 2.8,
    "V": 0.98,
    "W": 2.4,
    "X": 0.15,
    "Y": 2.0,
    "Z": 0.074,
}
LETTERS = CHAR_FREQ_DICT.keys()

def decode_single_xor_msg(h):
    msg_scores = {}
    for c in LETTERS:
        oc = c
        c = hexlify(c.encode()) * len(h)
        s = xor(c, h)
        s = unhexlify(s).decode()
        s = s[34:]
        score = get_char_freq_score(s)
        msg_scores[float(score)] = (str(s), str(oc), float(score))
    best_score = max(list(msg_scores.keys()))
    return msg_scores[best_score]

def xor_msg(k, msg):
    res = b""
    for char in msg:
        res += bytes([char ^ k])
    return res

def decode_single_char_xor(h):
    msg_key_score = {}
    for i in range(256):
        res = xor_msg(i, h)
        score = char_freq_score(res)
        msg_key_score[float(score)] = (res, chr(i), float(score))
    max_score = max(list(msg_key_score.keys()))
    return msg_key_score[max_score]

def decode_single_char_xor_alpha(h):
    msg_key_score = {}
    for i in LETTERS:
        res = xor_msg(ord(i), h)
        score = char_freq_score(res)
        msg_key_score[float(score)] = (res, chr(ord(i)), float(score))
    max_score = max(list(msg_key_score.keys()))
    return msg_key_score[max_score]

def single_char_xor(b: bytes):
    msg_key_score = {}
    for i in range(256):
        res = xor_msg(i, b)
        score = char_freq_score(res)
        msg_key_score[float(score)] = (res, i, float(score))
    max_score = max(list(msg_key_score.keys()))
    return msg_key_score[max_score]

def get_char_freq_score(s: str):
    score = 0
    for i in s.split():
        try:
            score += CHAR_FREQ_DICT[i]
        except KeyError:
            pass
    return score

def char_freq_score(b: bytes):
    score = 0
    for i in b:
        try:
            score += CHAR_FREQ_DICT.get(chr(i), 0)
        except KeyError:
            pass
    return score

def repeat_key_encrypt(h: str, k: str):
    res = b""
    blocks = [h[i:i+len(k)] for i in range(0, len(h), len(k))]
    k_blocks = [k[i] for i in range(len(k))]
    enc_seq = [[xor_bytes(i, j) for i, j in zip(block, k_blocks)] for block in blocks]
    for seq in enc_seq:
        for b in seq:
            res += b
    return res.hex()

def repeat_key_xor(h: str, k: str):
    res = b""
    blocks = [h[i:i+len(k)] for i in range(0, len(h), len(k))]
    k_blocks = [k[i] for i in range(len(k))]
    enc_seq = [[xor_bytes(i, j) for i, j in zip(block, k_blocks)] for block in blocks]
    for seq in enc_seq:
        for b in seq:
            res += b
    return res

def hamming_dist_str(s1, s2):
    d = 0
    for i, j in zip(s1, s2):
        if i != j:
            d += 1
    return d

def hamming_dist_bits(s1, s2):
    d = 0
    if type(s1) == bytes:
        s1 = s1.decode()
    if type(s2) == bytes:
        s2 = s2.decode()
    s1 = char2bin(s1)[2:]
    s2 = char2bin(s2)[2:]
    for i, j in zip(s1, s2):
        if i != j:
            d += 1
    return d

def encrypt_cbc(text, key):
    bs = 16
    key = sha256(key.encode()).digest()
    pl = lambda s: bs - len(s) % bs
    pad = lambda s: s + pl(s) * bytes([pl(s)])
    encodeAES = lambda c, i, s: c.encrypt(pad(s.encode()))
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = encodeAES(cipher, iv, text)
    return base64.b64encode(iv + ct).decode()

def decrypt_cbc(data, key): 
    data = base64.b64decode(data)
    iv = data[:16] 
    ct = data[16:]
    key = sha256(key.encode()).digest()
    unpad = lambda pd: pd[:-pd[-1]]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decodeAES = unpad(cipher.decrypt(ct)).decode()
    return decodeAES

def xor(x, y):
    res = int(x, 16) ^ int(y, 16)
    return "%x" %res

def all_ascii(s):
    only_ascii_found = True
    for c in range(len(s)):
        if 32 <= ord(s[c]) < 127:
            continue
        else:
            only_ascii_found = False
            break
    return only_ascii_found

def chunkify_text_file(filename: str, chunk_size: int):
    chunk_dict = {}
    with open(filename, "r") as fh:
        data = fh.read()
    last_idx = len(data) - chunk_size -1
    for i in range(0, last_idx, chunk_size):
        chunk = data[i:i+chunk_size]
        chunk_dict[i] = chunk
    return chunk_dict

def chunkify_data(data: str, chunk_size: int):
    chunk_dict = {}
    last_idx = len(data) - chunk_size -1
    for i in range(0, last_idx, chunk_size):
        chunk = data[i:i+chunk_size]
        chunk_dict[i] = chunk
    return chunk_dict

def h2b64(h):
    if type(h) == bytes:
        h = bytes.fromhex(h.decode())
    else:
        h = bytes.fromhex(h)
    x = base64.b64encode(h)
    return x

def xor_hex_str(h1, h2):
    x = h2b64(h1)
    y = h2b64(h2)
    res = int.from_bytes(x, byteorder="big") ^ int.from_bytes(y, byteorder="big")
    return hex(res)[2:]

def xor_bytes(x, y):
    if type(x) == str:
        x = ord(x)
    if type(y) == str:
        y =  ord(y)
    res = bytes([x ^ y])
    return res

def char2bin(c: str, byteorder="big"):
    i = int.from_bytes(bytes(c.encode()), byteorder=byteorder)
    return bin(i)

def chunkify_str(s: str, chunk_size: int):
    chunks = [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]
    return chunks

def str2arr(s: str):
    return [s[i] for i in range(len(s))]

def align_data(data, bs=16):
    if len(data) % bs == 0:
        return data
    pad_size = (bs - (len(data) % bs)) % bs
    return data + bytes(pad_size)