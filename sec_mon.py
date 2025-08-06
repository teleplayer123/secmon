from device_analysis import *

import matplotlib.pyplot as plt
import os
import pandas as pd
import time

class SecMonInfo:

    def cpu_stats(self, block_interval=5):
        cpu = CpuUsage()
        cpu_stats = cpu.cpu_usage(block_interval=block_interval)
        return cpu_stats
    
    def mem_stats(self):
        mem = MemoryUsage()
        mem_stats = mem.mem_usage()
        return mem_stats
    
    def disk_stats(self):
        mem = MemoryUsage()
        disk_stats = mem.disk_usage()
        return disk_stats
    
    def net_stats(self, block_interval=5):
        net = NetworkUsage()
        stats = net.measure_usage(block_interval=block_interval)
        return stats
    
    def net_socket_stats(self, net_type="inet"):
        net = NetworkUsage()
        sock_info = net.network_sockets(net_type=net_type)
        return sock_info
    
class SecMon:

    def __init__(self, **kwargs):
        self.sec_info = SecMonInfo()
        self._kwargs = kwargs

    def get_device_stats(self, block_interval=5, duration=60):
        device_stats = {}
        end_time = time.time() + duration
        while time.time() < end_time:
            cpu = self.sec_info.cpu_stats(block_interval=block_interval)
            mem = self.sec_info.mem_stats()
            device_stats[int(time.time())] = {
                "cpu": cpu,
                "mem": mem,
            }
        return device_stats
    
    def graph_device_stats(self, block_interval=5, duration=60):
        stats = self.get_device_stats(block_interval=block_interval, duration=duration)
        times = list(stats.keys())
        cpu_usages = [stats[t]["cpu"]["cpu_utilization"] for t in times]
        mem_usages = [stats[t]["mem"]["virtual_memory"]["pct_memory_used"] for t in times]
        self._graph_cpu_stats(cpu_usages)

    def _graph_cpu_stats(self, cpu_stats):
        df = pd.DataFrame(cpu_stats)
        fig, ax = plt.subplots(figsize=(12, 8))
        x_labels = df.index
        cores = df.columns.tolist()
        plt.xticks(ticks=range(len(x_labels)), labels=x_labels)
        for i in range(len(cores)):
            plt.plot(range(len(x_labels)), df[cores[i]], label=cores[i])
        plt.legend()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"cpu_usage_{int(time.time())}.png")
            fig.savefig(filename)
            print(f"Saved CPU usage graph to {filename}")
        plt.show()

    def get_net_stats(self, block_interval=5, duration=60):
        net = NetworkUsage()
        net_usage = {}
        end_time = time.time() + duration
        while time.time() < end_time:
            usage = net.measure_usage(block_interval=block_interval)
            net_usage[int(time.time())] = usage
        return net_usage
    
    def graph_net_stats(self, block_interval=5, duration=60):
        net_usage = self.get_net_stats(block_interval=block_interval, duration=duration)
        times = list(net_usage.keys())
        