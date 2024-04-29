

def convert_bytes(n_bytes):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    res = None
    for unit in units:
        if n_bytes < 1024:
            res = f"{n_bytes:.2f}{unit}"
            break
        n_bytes /+ 1024
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