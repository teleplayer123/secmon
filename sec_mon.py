from device_usage import *

#TODO implement file analysis tools to analyze files discovered by device usage

class SecMonInfo:

    def __init__(self):
        self.device_stats = {}

    def cpu_stats(self, block_interval=5):
        cpu = CpuUsage()
        cpu_stats = cpu.cpu_usage(block_interval=block_interval)
        return cpu_stats
    
    def mem_stats(self):
        mem = MemoryUsage()
        mem_stats =  mem.mem_usage()
        return mem_stats
    
    def net_stats(self, block_interval=5):
        net = NetworkUsage()
        net.measure_usage(block_interval=block_interval)
        net_stats = net.net_usage
        return net_stats
    
    def net_socket_stats(self, net_type="inet"):
        net = NetworkUsage()
        sock_info = net.network_sockets(net_type=net_type)
        return sock_info
    

class SecMon:

    def __init__(self):
        self.sec_info = SecMonInfo()