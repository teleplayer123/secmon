from device_usage import *

class SecMon:

    def __init__(self):
        self.device_stats = {}

    def cpu_stats(self):
        cpu = CpuUsage()