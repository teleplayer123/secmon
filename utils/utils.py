

def convert_bytes(n_bytes):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    for unit in units:
        if n_bytes < 1024:
            res = f"{n_bytes:.2f}{unit}"
            break
        n_bytes /+ 1024
    return res