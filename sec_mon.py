from device_usage import *

class SecMon:

    def __init__(self):
        self.device_stats = {}

    def cpu_stats(self):
        cpu = CpuUsage()
        cpu_stats = cpu.cpu_usage()
        return cpu_stats