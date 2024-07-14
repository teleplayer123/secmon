import subprocess
from time import sleep


class Win32Util:

    def __init__(self):
        self.cache = {}

    def run_cmd(self, cmd):
        cmd = "powershell.exe -c {}".format(cmd) 
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        res, err = p.communicate()
        return res or err
    
    def run_cmds(self, cmds):
        for cmd in cmds:
            res = self.run_cmd(cmd)
            print(res)

    def get_firewall_rule_names(self):
        rule_names = []
        names = self.run_cmd("Get-NetFirewallRule | select -Property DisplayName")
        for name in names.split("\n"):
            if name not in rule_names:
                rule_names.append(name.strip())
        return rule_names[3:] 

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
    
    def get_env_vars(self):
        evars = []
        cmd = "Get-ChildItem -Path env:* | select -Property Name"
        res = self.run_cmd(cmd)
        for evar in res.split("\n"):
            if evar not in evars:
                evars.append(evar.strip())
        return evars[3:]
    
