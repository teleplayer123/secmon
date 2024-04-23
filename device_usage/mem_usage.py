import psutil
from utils.utils import convert_bytes

class MemoryUsage:

    def __init__(self):
        self.mem_stats = {}

    def memory_stats(self):
        #memory info
        vmem_stats = {}
        vmem = psutil.virtual_memory()
        vmem_stats["available_memory"] = convert_bytes(vmem.available)
        vmem_stats["total_memory"] = convert_bytes(vmem.total)
        vmem_stats["pct_memory_used"] = convert_bytes(vmem.percent)
        vmem_stats["used_memory"] = convert_bytes(vmem.used)
        vmem_stats["free_memory"] = convert_bytes(vmem.free)
        self.mem_stats["virtual_memory"] = vmem_stats
        #swap memory info
        swap_mem = {}
        smem = psutil.swap_memory()
        swap_mem["total_swap_memory"] = convert_bytes(smem.total)