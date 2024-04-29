from device_usage import *

class SecMon:

    def __init__(self):
        self.device_stats = {}

    def cpu_stats(self, block_interval=1):
        cpu = CpuUsage(block_interval=block_interval)
        cpu_stats = cpu.cpu_usage
        return cpu_stats
    
    def mem_stats(self):
        mem = MemoryUsage()
        mem_stats =  mem.mem_usage
        return mem_stats
    
    def net_stats(self, block_interval=5):
        net = NetworkUsage()
        net_stats = net.measure_usage(block_interval=block_interval)
        return net_stats