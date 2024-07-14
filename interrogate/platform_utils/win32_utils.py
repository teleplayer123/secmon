import subprocess


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