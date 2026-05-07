from device_analysis import *

import argparse
import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import pandas as pd
import psutil
import seaborn as sns
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

    def get_device_stats(self, block_interval=5, duration=20):
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
        self._graph_cpu_stats(cpu_usages, timestamps=times)
        self._graph_mem_stats(mem_usages, timestamps=times)

    def _graph_cpu_stats(self, cpu_stats, timestamps=None):
        sns.set_theme(style="darkgrid", palette="muted")
        df = pd.DataFrame(cpu_stats)
        df.columns = [f"Core {c}" for c in df.columns]
        n_samples = len(df)

        if timestamps and len(timestamps) == n_samples:
            x_labels = [datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S") for t in timestamps]
        else:
            x_labels = [str(i) for i in range(n_samples)]

        palette = sns.color_palette("tab10", n_colors=len(df.columns))
        fig, ax = plt.subplots(figsize=(14, 6))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#16213e")

        for idx, col in enumerate(df.columns):
            ax.plot(range(n_samples), df[col], label=col, color=palette[idx], linewidth=1.8)
            ax.fill_between(range(n_samples), df[col], alpha=0.08, color=palette[idx])

        tick_step = max(1, n_samples // 10)
        ax.set_xticks(range(0, n_samples, tick_step))
        ax.set_xticklabels(x_labels[::tick_step], rotation=30, ha="right", fontsize=8, color="#c9d1d9")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
        ax.set_ylim(0, 105)

        ax.set_title("CPU Utilization per Core", fontsize=15, fontweight="bold", color="#e6edf3", pad=14)
        ax.set_xlabel("Time", fontsize=11, color="#8b949e", labelpad=8)
        ax.set_ylabel("Utilization", fontsize=11, color="#8b949e", labelpad=8)
        ax.tick_params(colors="#8b949e")
        for spine in ax.spines.values():
            spine.set_edgecolor("#30363d")
        ax.grid(color="#30363d", linewidth=0.6, alpha=0.7)

        legend = ax.legend(
            loc="upper right", fontsize=8, framealpha=0.3,
            facecolor="#0d1117", edgecolor="#30363d", labelcolor="#c9d1d9",
            ncol=max(1, len(df.columns) // 8),
        )

        avg_util = df.mean(axis=1).mean()
        ax.annotate(
            f"Mean utilization: {avg_util:.1f}%",
            xy=(0.01, 0.96), xycoords="axes fraction",
            fontsize=9, color="#58a6ff",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0d1117", alpha=0.6, edgecolor="#30363d"),
        )

        plt.tight_layout()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"cpu_usage_{int(time.time())}.png")
            fig.savefig(filename, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
            print(f"Saved CPU usage graph to {filename}")
        plt.show()

    def _graph_mem_stats(self, mem_stats, timestamps=None):
        sns.set_theme(style="darkgrid", palette="muted")
        pct_vals = [float(v.strip("%")) for v in mem_stats]
        n_samples = len(pct_vals)

        if timestamps and len(timestamps) == n_samples:
            x_labels = [datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S") for t in timestamps]
        else:
            x_labels = [str(i) for i in range(n_samples)]

        xs = range(n_samples)
        fig, ax = plt.subplots(figsize=(14, 4))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#16213e")

        color_used = "#f0883e"
        ax.plot(xs, pct_vals, color=color_used, linewidth=2.2, label="Memory Used %")
        ax.fill_between(xs, pct_vals, alpha=0.25, color=color_used)

        ax.axhline(y=80, color="#ff6b6b", linewidth=1.0, linestyle="--", alpha=0.7, label="80% threshold")

        tick_step = max(1, n_samples // 10)
        ax.set_xticks(range(0, n_samples, tick_step))
        ax.set_xticklabels(x_labels[::tick_step], rotation=30, ha="right", fontsize=8, color="#c9d1d9")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
        ax.set_ylim(0, 105)

        ax.set_title("Memory Utilization", fontsize=15, fontweight="bold", color="#e6edf3", pad=14)
        ax.set_xlabel("Time", fontsize=11, color="#8b949e", labelpad=8)
        ax.set_ylabel("% Used", fontsize=11, color="#8b949e", labelpad=8)
        ax.tick_params(colors="#8b949e")
        for spine in ax.spines.values():
            spine.set_edgecolor("#30363d")
        ax.grid(color="#30363d", linewidth=0.6, alpha=0.7)

        ax.legend(
            loc="upper right", fontsize=9, framealpha=0.3,
            facecolor="#0d1117", edgecolor="#30363d", labelcolor="#c9d1d9",
        )

        peak = max(pct_vals)
        avg = sum(pct_vals) / len(pct_vals)
        ax.annotate(
            f"Avg: {avg:.1f}%  |  Peak: {peak:.1f}%",
            xy=(0.01, 0.92), xycoords="axes fraction",
            fontsize=9, color="#58a6ff",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0d1117", alpha=0.6, edgecolor="#30363d"),
        )

        plt.tight_layout()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"mem_usage_{int(time.time())}.png")
            fig.savefig(filename, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
            print(f"Saved memory usage graph to {filename}")
        plt.show()

    def get_net_stats(self, block_interval=5, duration=20):
        net = NetworkUsage()
        net_usage = {}
        end_time = time.time() + duration
        while time.time() < end_time:
            usage = net.measure_usage(block_interval=block_interval)
            net_usage[int(time.time())] = usage
        return net_usage

    def graph_net_stats(self, block_interval=5, duration=20):
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
        sns.set_theme(style="darkgrid", palette="muted")
        n_samples = len(times)
        x_labels = [datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S") for t in times]
        xs = range(n_samples)
        ifaces = list(rx_by_iface.keys())
        palette = sns.color_palette("tab10", n_colors=len(ifaces))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True)
        fig.patch.set_facecolor("#1a1a2e")

        _DARK_BG = "#16213e"
        _GRID = "#30363d"
        _LABEL = "#8b949e"
        _TEXT = "#e6edf3"
        _TICK = "#c9d1d9"
        _ANNOT = "#58a6ff"

        for ax, data_by_iface, direction, color_offset in [
            (ax1, rx_by_iface, "Download (RX)", 0),
            (ax2, tx_by_iface, "Upload (TX)", 0),
        ]:
            ax.set_facecolor(_DARK_BG)
            for idx, iface in enumerate(ifaces):
                vals = data_by_iface[iface]
                ax.plot(xs, vals, label=iface, color=palette[idx], linewidth=2.0)
                ax.fill_between(xs, vals, alpha=0.12, color=palette[idx])
            ax.set_title(f"Network {direction}", fontsize=13, fontweight="bold", color=_TEXT, pad=10)
            ax.set_ylabel("Mbps", fontsize=11, color=_LABEL, labelpad=8)
            ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
            ax.tick_params(colors=_TICK, labelsize=8)
            for spine in ax.spines.values():
                spine.set_edgecolor(_GRID)
            ax.grid(color=_GRID, linewidth=0.6, alpha=0.7)
            ax.legend(
                loc="upper right", fontsize=8, framealpha=0.3,
                facecolor="#0d1117", edgecolor=_GRID, labelcolor=_TICK,
            )

        tick_step = max(1, n_samples // 10)
        ax2.set_xticks(range(0, n_samples, tick_step))
        ax2.set_xticklabels(x_labels[::tick_step], rotation=30, ha="right", fontsize=8, color=_TICK)
        ax2.set_xlabel("Time", fontsize=11, color=_LABEL, labelpad=8)

        all_rx = [v for vals in rx_by_iface.values() for v in vals]
        all_tx = [v for vals in tx_by_iface.values() for v in vals]
        peak_rx = max(all_rx) if all_rx else 0
        peak_tx = max(all_tx) if all_tx else 0
        ax1.annotate(
            f"Peak RX: {peak_rx:.3f} Mbps",
            xy=(0.01, 0.92), xycoords="axes fraction",
            fontsize=9, color=_ANNOT,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0d1117", alpha=0.6, edgecolor=_GRID),
        )
        ax2.annotate(
            f"Peak TX: {peak_tx:.3f} Mbps",
            xy=(0.01, 0.92), xycoords="axes fraction",
            fontsize=9, color=_ANNOT,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0d1117", alpha=0.6, edgecolor=_GRID),
        )

        fig.suptitle("Network Throughput by Interface", fontsize=16, fontweight="bold", color=_TEXT, y=1.01)
        plt.tight_layout()
        if self._kwargs.get("save_graph") == True:
            filename = os.path.join(os.getcwd(), f"net_usage_{int(time.time())}.png")
            fig.savefig(filename, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
            print(f"Saved network usage graph to {filename}")
        plt.show()

    def get_disk_stats(self):
        return self.sec_info.disk_stats()

    def get_socket_stats(self, net_type="inet"):
        return self.sec_info.net_socket_stats(net_type=net_type)


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="secmon",
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
        default=20,
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
        default=20,
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
