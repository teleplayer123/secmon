from device_analysis import *

import argparse
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import psutil
import sys
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
        self._graph_mem_stats(mem_usages)

    def _graph_cpu_stats(self, cpu_stats):
        df = pd.DataFrame(cpu_stats)
        fig, ax = plt.subplots(figsize=(12, 8))
        x_labels = df.index
        cores = df.columns.tolist()
        ax.set_title("CPU Utilization per Core (%)")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Utilization (%)")
        plt.xticks(ticks=range(len(x_labels)), labels=x_labels)
        for i in range(len(cores)):
            plt.plot(range(len(x_labels)), df[cores[i]], label=f"Core {cores[i]}")
        plt.legend()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"cpu_usage_{int(time.time())}.png")
            fig.savefig(filename)
            print(f"Saved CPU usage graph to {filename}")
        plt.show()

    def _graph_mem_stats(self, mem_stats):
        pct_vals = [float(v.strip("%")) for v in mem_stats]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(range(len(pct_vals)), pct_vals, label="Memory Used %", color="orange")
        ax.set_title("Memory Usage (%)")
        ax.set_xlabel("Sample")
        ax.set_ylabel("% Used")
        ax.set_ylim(0, 100)
        ax.legend()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"mem_usage_{int(time.time())}.png")
            fig.savefig(filename)
            print(f"Saved memory usage graph to {filename}")
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
        if not times:
            print("No network data collected.")
            return
        ifaces = list(net_usage[times[0]].keys())
        rx_by_iface = {iface: [net_usage[t][iface]["rx"] for t in times] for iface in ifaces}
        tx_by_iface = {iface: [net_usage[t][iface]["tx"] for t in times] for iface in ifaces}
        self._graph_net_data(times, rx_by_iface, tx_by_iface)

    def _graph_net_data(self, times, rx_by_iface, tx_by_iface):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        x = range(len(times))
        for iface, rx_vals in rx_by_iface.items():
            ax1.plot(x, rx_vals, label=iface)
        ax1.set_title("Network RX (Mbps)")
        ax1.set_xlabel("Sample")
        ax1.set_ylabel("Mbps")
        ax1.legend()
        for iface, tx_vals in tx_by_iface.items():
            ax2.plot(x, tx_vals, label=iface)
        ax2.set_title("Network TX (Mbps)")
        ax2.set_xlabel("Sample")
        ax2.set_ylabel("Mbps")
        ax2.legend()
        plt.tight_layout()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"net_usage_{int(time.time())}.png")
            fig.savefig(filename)
            print(f"Saved network usage graph to {filename}")
        plt.show()

    def get_disk_stats(self):
        return self.sec_info.disk_stats()

    def get_socket_stats(self, net_type="inet"):
        return self.sec_info.net_socket_stats(net_type=net_type)


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="sec_mon",
        description="Security monitoring tool for device, network, and file analysis.",
    )
    parser.add_argument(
        "--save-graph",
        action="store_true",
        help="Save generated graphs to PNG files in the current directory",
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # --- device ---
    p = sub.add_parser("device", help="Snapshot of CPU and memory stats")
    p.add_argument(
        "--block-interval",
        type=int,
        default=1,
        metavar="SECS",
        help="Seconds to sample CPU utilization (default: 1)",
    )

    # --- disk ---
    sub.add_parser("disk", help="Disk usage per mount point")

    # --- net ---
    p = sub.add_parser("net", help="Snapshot of network interface throughput")
    p.add_argument(
        "--block-interval",
        type=int,
        default=1,
        metavar="SECS",
        help="Seconds to sample throughput (default: 1)",
    )

    # --- sockets ---
    p = sub.add_parser("sockets", help="Active network socket connections")
    p.add_argument(
        "--type",
        default="inet",
        choices=["inet", "inet4", "inet6", "tcp", "tcp4", "tcp6", "udp", "udp4", "udp6", "unix", "all"],
        metavar="KIND",
        help="Socket family filter passed to psutil (default: inet). "
             "Choices: inet inet4 inet6 tcp tcp4 tcp6 udp udp4 udp6 unix all",
    )

    # --- graph-device ---
    p = sub.add_parser("graph-device", help="Graph CPU and memory usage over time")
    p.add_argument(
        "--block-interval",
        type=int,
        default=5,
        metavar="SECS",
        help="Seconds per CPU sample (default: 5)",
    )
    p.add_argument(
        "--duration",
        type=int,
        default=60,
        metavar="SECS",
        help="Total monitoring duration in seconds (default: 60)",
    )

    # --- graph-net ---
    p = sub.add_parser("graph-net", help="Graph network RX/TX usage over time")
    p.add_argument(
        "--block-interval",
        type=int,
        default=5,
        metavar="SECS",
        help="Seconds per throughput sample (default: 5)",
    )
    p.add_argument(
        "--duration",
        type=int,
        default=60,
        metavar="SECS",
        help="Total monitoring duration in seconds (default: 60)",
    )

    # --- pcap ---
    p = sub.add_parser("pcap", help="Extract payload data from a .pcap file")
    p.add_argument("file", help="Path to the .pcap file")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    mon = SecMon(save_graph=args.save_graph)

    if args.command == "device":
        cpu = mon.sec_info.cpu_stats(block_interval=args.block_interval)
        mem = mon.sec_info.mem_stats()
        print(json.dumps({"cpu": cpu, "memory": mem}, indent=2))

    elif args.command == "disk":
        print(json.dumps(mon.get_disk_stats(), indent=2))

    elif args.command == "net":
        stats = mon.sec_info.net_stats(block_interval=args.block_interval)
        print(json.dumps(stats, indent=2))

    elif args.command == "sockets":
        try:
            print(json.dumps(mon.get_socket_stats(net_type=args.type), indent=2))
        except psutil.AccessDenied:
            print("Permission denied: run this option with sudo.")
            sys.exit(1)
    elif args.command == "graph-device":
        print(f"Collecting device stats for {args.duration}s (sample interval: {args.block_interval}s)…")
        mon.graph_device_stats(block_interval=args.block_interval, duration=args.duration)

    elif args.command == "graph-net":
        print(f"Collecting network stats for {args.duration}s (sample interval: {args.block_interval}s)…")
        mon.graph_net_stats(block_interval=args.block_interval, duration=args.duration)

    elif args.command == "pcap":
        if not os.path.isfile(args.file):
            print(f"error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        from utils.extract_pcap_data import extract_pcap_data
        try:
            data = extract_pcap_data(args.file)
            print(data)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
