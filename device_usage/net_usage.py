import psutil
import time
from utils.utils import convert_bytes


class NetworkUsage:
    def __init__(self):
        self.ifaces = []
        self.counters = {}

    def get_io_counter(self, pernic=True):
        io = psutil.net_io_counters(pernic=pernic)
        return io
    
    def measure_usage(self, duration=5):
        io1 = self.get_io_counter()
        time.sleep(duration)
        io2 = self.get_io_counter()
        ifaces = list(io1.keys())
        #self.ifaces.append(iface for iface in ifaces if iface not in self.ifaces)
        for iface in ifaces:
            rx = convert_bytes(io2[iface].bytes_recv - io1[iface].bytes_recv)
            tx = convert_bytes(io2[iface].bytes_sent - io1[iface].bytes_sent)
            self.counters[iface] = {"rx": rx, "tx": tx}

    def network_sockets(self, sock_type="inet"):
        nets = psutil.net_connections(kind="inet")