import psutil
from utils.utils import convert_bytes


class CpuUsage:

    def __init__(self, block_interval: int=1):
        self.cpu_stats = {}
        self.interval = block_interval

    def cpu_usage(self):
        stats_since_boot = {}
        boot_stats = psutil.cpu_stats()
        #context switch is a sequence of operations where the cpu stores state of a running process and loads the next process
        #context switching is essential for multitasking
        stats_since_boot["ctx_switches"] = boot_stats.ctx_switches
        #interrupts cause context switches that free up cpu time for other tasks
        stats_since_boot["interrupts"] = boot_stats.interrupts
        #software interrupt is requested by the processor upon executing particular instructions or when certain conditions are met
        stats_since_boot["soft_interrupts"] = boot_stats.soft_interrupts
        #number of systemcalls made since boot
        stats_since_boot["syscalls"] = boot_stats.syscalls
        self.cpu_stats["ctx_switches_since_boot"] = stats_since_boot

        #cpu performance frequency in MHz
        cpu_perf_stats = {}
        perf_stats = psutil.cpu_freq()
        cpu_perf_stats["current_freq"] = f"{perf_stats.current}MHz"
        cpu_perf_stats["min_freq"] = f"{perf_stats.min}MHz"
        cpu_perf_stats["max_freq"] = f"{perf_stats.max}MHz"
        self.cpu_stats = cpu_perf_stats

        #seconds cpu spent in each mode
        cpu_mode_times = {}
        mode_times = psutil.cpu_times(percpu=True)
        n_logical_cpus = len(mode_times)
        for i in range(1, len(n_logical_cpus)+1):
            cpu_mode_times[f"{i}"] = {
                "user_mode_time": f"{mode_times[i].user} secs",
                "system_mode_time": f"{mode_times[i].system} secs",
                "idle_mode_time": f"{mode_times[i].idle} secs",
                "interrupt_mode_time": f"{mode_times[i].interrupt} secs",
                "dpc_mode_time": f"{mode_times[i].dpc} secs"
            }
        self.cpu_stats["time_cpu_in_modes"] = cpu_mode_times

        #cpu utilization percentage
        cpu_util_pct = {}
        util_pct = psutil.cpu_percent(percpu=True, interval=self.interval)
        n_cpus = len(util_pct)
        for i in range(1, len(n_cpus)+1):
            cpu_util_pct[f"{i}"] = f"{util_pct[i]}%"
        self.cpu_stats["cpu_utilization"] = cpu_util_pct
        self.cpu_stats["available_cpus"] = len(psutil.Process().cpu_affinity())
        cpu_loads = psutil.getloadavg()
        avg_cpu_load = {
            "last_1min": cpu_loads[0],
            "last_5min": cpu_loads[1],
            "last_15min": cpu_loads[2]
        }
        self.cpu_stats["cpu_load_avg"] = avg_cpu_load
        
