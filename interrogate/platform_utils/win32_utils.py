import subprocess
from time import sleep


class Win32Util:

    def __init__(self):
        self.cache = {}

    def run_cmd(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="latin-1")
        res, err = p.communicate()
        return res or err
    
    def list_services(self):
        cmd = "powershell.exe reg query \"HKLM\\SYSTEM\\CurrentControlSet\\services\""
        return self.run_cmd(cmd)
    
    def get_wifi_log(self):
        cmd = "powershell.exe Get-WinEvent -Path C:\\Windows\\System32\\LogFiles\\WMI\\Wifi.etl -Oldest > test_wifi.txt"
        res = self.run_cmd(cmd)
        return res

    def win_pkt_cap(self, ip, proto="TCP", cap_time=10):
        subprocess.check_output(f"pktmon filter add -i {ip} -t {proto}", shell=True, encoding="utf-8")
        subprocess.check_output("pktmon start --etw", shell=True, encoding="utf-8")
        sleep(cap_time)
        file_info = subprocess.check_output("pktmon stop", shell=True, encoding="utf-8")
        file_info = file_info.split("\n")[-2]
        cap_file = file_info.split(" ")[2]
        res = subprocess.check_output(f"pktmon etl2txt {cap_file}", shell=True, encoding="utf-8")
        return res