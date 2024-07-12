import psutil


class ProcessUsage:

    def __init__(self):
        self.cache = {}

    def iter_win_svcs(self):
        running_svcs = []
        for p in psutil.win_service_iter():
            running_svcs.append(p)
        return running_svcs