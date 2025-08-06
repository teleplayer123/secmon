import psutil


class ProcessUsage:

    def __init__(self):
        self.running_services = {}

    def iter_win_svcs(self):
        svcs = {}
        for p in psutil.win_service_iter():
            try:
                d = p.as_dict()
                svcs[p.name()] = {
                    "display_name": d["display_name"],
                    "binpath": d["binpath"],
                    "username": d["username"],
                    "start_type": d["start_type"],
                    "status": d["status"],
                    "pid": d["pid"],
                    "name": d["name"],
                    "description": d["description"]
                }
            except FileNotFoundError:
                continue
        return svcs