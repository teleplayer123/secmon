import subprocess
from time import sleep


class Win32Util:

    def __init__(self):
        self.cache = {}

    def run_cmd(self, cmd):
        cmd = "powershell.exe {}".format(cmd) 
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf-8")
        res, err = p.communicate()
        return res or err
    
    def run_cmds(self, cmds):
        for cmd in cmds:
            res = self.run_cmd(cmd)
            print(res)

    def list_services(self):
        cmd = "reg query \"HKLM\\SYSTEM\\CurrentControlSet\\services\""
        return self.run_cmd(cmd)
    
    def get_wifi_log(self):
        cmd = "Get-WinEvent -Path C:\\Windows\\System32\\LogFiles\\WMI\\Wifi.etl -Oldest > test_wifi.txt"
        res = self.run_cmd(cmd)
        return res

    def win_pkt_cap(self, ip, proto="TCP", cap_time=10):
        """requires admin privilages"""
        cmds = [f"pktmon filter add -i {ip} -t {proto}", "pktmon start --etw"]
        self.run_cmds(cmds)
        sleep(cap_time)
        file_info = self.run_cmd("pktmon stop")
        file_info = file_info.split("\n")[-2]
        cap_file = file_info.split(" ")[2]
        res = self.run_cmd(f"pktmon etl2txt {cap_file}")
        return res
    
