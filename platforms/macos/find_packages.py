import os
import plistlib
import subprocess
from pathlib import Path

import psutil


_APP_DIRS = [
    "/Applications",
    "/System/Applications",
    "/System/Applications/Utilities",
    str(Path.home() / "Applications"),
]

# Directories managed by Homebrew — used to exclude their binaries from CLI tool discovery.
_HOMEBREW_DIRS = {
    "/opt/homebrew/bin",
    "/opt/homebrew/sbin",
    "/usr/local/Cellar",
    "/opt/homebrew/Cellar",
}

_CLI_DIRS = [
    "/usr/bin",
    "/usr/sbin",
    "/usr/local/bin",
    "/usr/local/sbin",
]


class MacOSAppFinder:
    """
    Discovers programs installed on macOS through native channels:
      - .app bundles (GUI applications, including Mac App Store)
      - pkgutil system packages (macOS installer / .pkg)
      - CLI executables in standard non-Homebrew binary directories
    """

    # ------------------------------------------------------------------
    # App bundles
    # ------------------------------------------------------------------

    def find_app_bundles(self) -> list[dict]:
        """
        Scan standard application directories for .app bundles.

        Parses each bundle's Info.plist to extract name, bundle ID,
        version, and executable path. Also detects Mac App Store apps
        by the presence of a _MASReceipt directory inside the bundle.
        """
        apps = []
        seen: set[str] = set()
        for app_dir in _APP_DIRS:
            if not os.path.isdir(app_dir):
                continue
            try:
                entries = list(os.scandir(app_dir))
            except PermissionError:
                continue
            for entry in entries:
                try:
                    if not entry.name.endswith(".app") or not entry.is_dir(follow_symlinks=True):
                        continue
                    real = os.path.realpath(entry.path)
                except PermissionError:
                    continue
                if real in seen:
                    continue
                seen.add(real)
                apps.append(self._parse_app_bundle(entry.path))
        return apps

    def _parse_app_bundle(self, app_path: str) -> dict:
        info = {
            "name": os.path.basename(app_path).removesuffix(".app"),
            "path": app_path,
            "source": "app_bundle",
            "bundle_id": None,
            "version": None,
            "executable": None,
            "mas_app": False,
        }
        contents = os.path.join(app_path, "Contents")
        plist_path = os.path.join(contents, "Info.plist")
        if os.path.isfile(plist_path):
            try:
                with open(plist_path, "rb") as f:
                    plist = plistlib.load(f)
                info["bundle_id"] = plist.get("CFBundleIdentifier")
                info["version"] = (
                    plist.get("CFBundleShortVersionString") or plist.get("CFBundleVersion")
                )
                exec_name = plist.get("CFBundleExecutable")
                if exec_name:
                    info["executable"] = os.path.join(contents, "MacOS", exec_name)
            except Exception:
                pass

        # Mac App Store apps have a receipt directory inside the bundle.
        if os.path.isdir(os.path.join(contents, "_MASReceipt")):
            info["mas_app"] = True
            info["source"] = "mas"

        return info

    # ------------------------------------------------------------------
    # pkgutil — macOS installer / .pkg packages
    # ------------------------------------------------------------------

    def find_system_packages(self, include_details: bool = False) -> list[dict]:
        """
        Enumerate packages registered with pkgutil (macOS installer packages).

        Set include_details=True to query install location and version for
        each package (slow — one subprocess call per package).
        """
        try:
            result = subprocess.run(
                ["pkgutil", "--pkgs"],
                capture_output=True, text=True, timeout=30,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []

        packages = []
        for pkg_id in result.stdout.strip().splitlines():
            pkg_id = pkg_id.strip()
            if not pkg_id:
                continue
            entry = {
                "name": pkg_id,
                "bundle_id": pkg_id,
                "source": "pkgutil",
                "version": None,
                "path": None,
                "executable": None,
            }
            if include_details:
                entry.update(self._pkgutil_info(pkg_id))
            packages.append(entry)
        return packages

    def _pkgutil_info(self, pkg_id: str) -> dict:
        try:
            result = subprocess.run(
                ["pkgutil", "--pkg-info", pkg_id],
                capture_output=True, text=True, timeout=10,
            )
            details: dict = {}
            for line in result.stdout.splitlines():
                if line.startswith("version:"):
                    details["version"] = line.split(":", 1)[1].strip()
                elif line.startswith("location:"):
                    details["path"] = line.split(":", 1)[1].strip()
            return details
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {}

    # ------------------------------------------------------------------
    # CLI tools (non-Homebrew)
    # ------------------------------------------------------------------

    def find_cli_tools(self) -> list[dict]:
        """
        Find executable files in standard non-Homebrew binary directories.

        Symlinks that resolve into a Homebrew-managed directory are excluded
        so only natively installed or OS-bundled tools are returned.
        """
        tools = []
        seen: set[str] = set()
        for bin_dir in _CLI_DIRS:
            if not os.path.isdir(bin_dir):
                continue
            try:
                entries = list(os.scandir(bin_dir))
            except PermissionError:
                continue
            for entry in entries:
                try:
                    if not entry.is_file(follow_symlinks=True):
                        continue
                    if not os.access(entry.path, os.X_OK):
                        continue
                    real = os.path.realpath(entry.path)
                except PermissionError:
                    continue
                if any(real.startswith(d) for d in _HOMEBREW_DIRS):
                    continue
                if real in seen:
                    continue
                seen.add(real)
                tools.append({
                    "name": entry.name,
                    "path": entry.path,
                    "source": "cli_tool",
                    "bundle_id": None,
                    "version": None,
                    "executable": entry.path,
                })
        return tools

    # ------------------------------------------------------------------
    # Combined discovery
    # ------------------------------------------------------------------

    def find_all(self, pkgutil_details: bool = False) -> dict:
        """
        Discover all natively installed programs and return them grouped by source.

        Keys: 'app_bundles', 'mas_apps', 'system_packages', 'cli_tools'.
        """
        bundles = self.find_app_bundles()
        return {
            "app_bundles": [b for b in bundles if not b["mas_app"]],
            "mas_apps": [b for b in bundles if b["mas_app"]],
            "system_packages": self.find_system_packages(include_details=pkgutil_details),
            "cli_tools": self.find_cli_tools(),
        }


class MacOSResourceAnalyzer:
    """
    Measures system resource consumption for installed macOS programs.

    Correlates discovered apps to live processes, then reports per-process
    CPU, memory, open files, network connections, and disk I/O.
    """

    def get_running_processes(self) -> list[dict]:
        """Snapshot of all running processes with basic resource metrics."""
        attrs = ["pid", "name", "exe", "status", "username", "cpu_percent", "memory_info"]
        procs = []
        for proc in psutil.process_iter(attrs):
            try:
                info = proc.info
                mem = info.get("memory_info")
                procs.append({
                    "pid": info["pid"],
                    "name": info["name"],
                    "exe": info["exe"],
                    "status": info["status"],
                    "username": info["username"],
                    "cpu_percent": info["cpu_percent"],
                    "memory_rss_mb": round(mem.rss / 1024 / 1024, 2) if mem else None,
                    "memory_vms_mb": round(mem.vms / 1024 / 1024, 2) if mem else None,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return procs

    def get_process_resources(self, pid: int, cpu_interval: float = 1.0) -> dict:
        """
        Detailed resource snapshot for a single process.

        cpu_interval controls how long psutil samples CPU utilization (seconds).
        Fields that require elevated privileges are set to None on access denial.
        """
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                mem = proc.memory_info()
                cpu = proc.cpu_percent(interval=cpu_interval)

                try:
                    open_files = [f.path for f in proc.open_files()]
                except psutil.AccessDenied:
                    open_files = None

                try:
                    connections = [
                        {
                            "family": c.family.name,
                            "type": c.type.name,
                            "local_addr": f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "",
                            "remote_addr": f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "",
                            "status": c.status,
                        }
                        for c in proc.net_connections()
                    ]
                except psutil.AccessDenied:
                    connections = None

                try:
                    io = proc.io_counters()
                    io_counters = {
                        "read_bytes": io.read_bytes,
                        "write_bytes": io.write_bytes,
                    }
                except (psutil.AccessDenied, AttributeError):
                    io_counters = None

                return {
                    "pid": pid,
                    "name": proc.name(),
                    "exe": proc.exe(),
                    "status": proc.status(),
                    "cpu_percent": cpu,
                    "memory_rss_mb": round(mem.rss / 1024 / 1024, 2),
                    "memory_vms_mb": round(mem.vms / 1024 / 1024, 2),
                    "open_files_count": len(open_files) if open_files is not None else None,
                    "open_files": open_files,
                    "network_connections": connections,
                    "io_counters": io_counters,
                }
        except psutil.NoSuchProcess:
            return {"error": f"no process with PID {pid}"}
        except psutil.AccessDenied:
            return {"error": f"access denied for PID {pid}"}

    def correlate_apps_to_processes(self, installed: list[dict]) -> list[dict]:
        """
        Match installed app dicts to live running processes.

        Matching priority:
          1. Exact executable path match
          2. Case-insensitive name match

        Each returned dict extends the input with 'running' (bool) and
        'process' (the matched process dict, or None).
        """
        running = self.get_running_processes()
        by_exe = {p["exe"]: p for p in running if p["exe"]}
        by_name: dict[str, list[dict]] = {}
        for p in running:
            if p["name"]:
                by_name.setdefault(p["name"].lower(), []).append(p)

        results = []
        for app in installed:
            match = None
            if app.get("executable") and app["executable"] in by_exe:
                match = by_exe[app["executable"]]
            elif app.get("name"):
                candidates = by_name.get(app["name"].lower(), [])
                if candidates:
                    match = candidates[0]
            results.append({**app, "running": match is not None, "process": match})
        return results

    def analyze_installed_apps(
        self, installed: list[dict], cpu_interval: float = 1.0
    ) -> list[dict]:
        """
        Full resource analysis for all installed apps that are currently running.

        Non-running apps get 'resources': None. Running apps get a full
        resource dict from get_process_resources().
        """
        correlated = self.correlate_apps_to_processes(installed)
        for app in correlated:
            if app["running"] and app["process"]:
                pid = app["process"]["pid"]
                app["resources"] = self.get_process_resources(pid, cpu_interval=cpu_interval)
            else:
                app["resources"] = None
        return correlated
