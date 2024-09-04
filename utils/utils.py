Bps2Mbps = lambda r: r / 125000
bps2Mbps = lambda r: r / 1e+6
Kbps2Mbps = lambda r: r / 1000
KBps2Mbps = lambda r: r / 125

def convert_bytes(n_bytes):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    res = None
    for unit in units:
        if n_bytes < 1024:
            res = f"{n_bytes:.2f}{unit}"
            break
        n_bytes /= 1024
    return res

#function from psutil _common.py
def bytes2human(n, format="%(value).1f%(symbol)s"):
    symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if abs(n) >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)

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