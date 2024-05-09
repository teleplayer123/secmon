import psutil
import time
from utils.utils import convert_bytes


class NetworkUsage:
    def __init__(self):
        self.ifaces = []
        self.net_usage = {}

    def get_io_counter(self, pernic=True):
        io = psutil.net_io_counters(pernic=pernic)
        return io
    
    def measure_usage(self, block_interval=5):
        io1 = self.get_io_counter()
        time.sleep(block_interval)
        io2 = self.get_io_counter()
        ifaces = list(io1.keys())
        self.ifaces.append(iface for iface in ifaces if iface not in self.ifaces)
        for iface in ifaces:
            rx = convert_bytes(io2[iface].bytes_recv - io1[iface].bytes_recv)
            tx = convert_bytes(io2[iface].bytes_sent - io1[iface].bytes_sent)
            self.net_usage[iface] = {"rx": rx, "tx": tx}

    def network_sockets(self, net_type="inet"):
        socket_info = {
            "tcp": [],
            "udp": []
        }
        nets = psutil.net_connections(kind=net_type)
        for net in nets:
            try:
                raddr = net.raddr.ip
                rport = net.raddr.port
            except AttributeError:
                raddr = ""
                rport = ""
            sock_dict = {
                    "family": net.family.name,
                    "local_addr": net.laddr.ip,
                    "local_port": net.laddr.port,
                    "remote_addr": raddr,
                    "remote_port": rport,
                    "pid": net.pid,
                    "status": net.status
            }
            if net.type.value == 1:
                socket_info["tcp"].append(sock_dict)
            elif net.type.value == 2:
                socket_info["udp"].append(sock_dict)
            else:
                print("unimplemented protocol: {}: {}".format(net.type.name, net.type.value))
                
        return socket_info
                
