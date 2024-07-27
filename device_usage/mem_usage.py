import psutil
from utils.utils import convert_bytes

class MemoryUsage:

    def __init__(self):
        self.cache = {}

    def mem_usage(self):
        mem_stats = {}
        #memory info
        vmem_stats = {}
        vmem = psutil.virtual_memory()
        vmem_stats["available_memory"] = convert_bytes(vmem.available)
        vmem_stats["total_memory"] = convert_bytes(vmem.total)
        vmem_stats["pct_memory_used"] = f"{vmem.percent}%"
        vmem_stats["used_memory"] = convert_bytes(vmem.used)
        vmem_stats["free_memory"] = convert_bytes(vmem.free)
        mem_stats["virtual_memory"] = vmem_stats
        #swap memory info
        swap_mem = {}
        smem = psutil.swap_memory()
        swap_mem["total_swap_memory"] = convert_bytes(smem.total)
        swap_mem["used_swap_memory"] = convert_bytes(smem.used)
        swap_mem["free_swap_memory"] = convert_bytes(smem.free)
        swap_mem["percent_used_swap_memory"] = f"{smem.percent}%"
        swap_mem["swapped_in_from_disk_memory"] = convert_bytes(smem.sin)
        swap_mem["swapped_out_from_disk_memory"] = convert_bytes(smem.sout)
        mem_stats["swap_memory"] = swap_mem
        return mem_stats
    
    def disk_usage(self):
        usage_dict = {}
        partitions = psutil.disk_partitions()
        for part in partitions:
            du = psutil.disk_usage(part.mountpoint)
            usage_dict[str(part.mountpoint)] = {
                "total": convert_bytes(du.total),
                "used": convert_bytes(du.used),
                "free": convert_bytes(du.free),
                "pct_used": du.percent
            }
        return usage_dict
