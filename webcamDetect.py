#Forked from https://gist.github.com/cobryan05/8e191ae63976224a0129a8c8f376adc6
import winreg
import psutil
import os

class WebcamDetect:
    REG_KEY = winreg.HKEY_CURRENT_USER
    WEBCAM_REG_SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam\\"
    WEBCAM_TIMESTAMP_VALUE_NAME = "LastUsedTimeStop"

    def __init__(self):
        self._regKey = winreg.OpenKey(WebcamDetect.REG_KEY, WebcamDetect.WEBCAM_REG_SUBKEY)

    def _get_exe_name(self, path_like_string: str):
        """Convert weird registry key string to executable name"""
        try:
            normal_path = path_like_string.replace('#', '\\')
            return os.path.basename(normal_path)
        except Exception:
            return path_like_string  # fallback

    def _get_pids_by_name(self, exe_name: str):
        exe_name = exe_name.lower()
        return [
            p.pid for p in psutil.process_iter(['name'])
            if p.info['name'] and p.info['name'].lower() == exe_name
        ]


    def getActiveApps(self):
        """Returns a list of (app_name, [pid1, pid2, ...]) tuples that are currently using the webcam."""

        def get_subkey_timestamp(subkey) -> int:
            try:
                value, _ = winreg.QueryValueEx(subkey, WebcamDetect.WEBCAM_TIMESTAMP_VALUE_NAME)
                return value
            except OSError:
                return None

        def get_pids_by_name(name: str):
            """Find all PIDs of processes with matching name (case-insensitive)"""
            name = name.lower()
            return [p.pid for p in psutil.process_iter(['name']) if p.info['name'] and p.info['name'].lower() == name]

        active_apps = []
        try:
            key = winreg.OpenKey(WebcamDetect.REG_KEY, WebcamDetect.WEBCAM_REG_SUBKEY)
            subkey_count, _, _ = winreg.QueryInfoKey(key)
            for idx in range(subkey_count):
                subkey_name = winreg.EnumKey(key, idx)
                subkey_path = f"{WebcamDetect.WEBCAM_REG_SUBKEY}\\{subkey_name}"
                subkey = winreg.OpenKey(WebcamDetect.REG_KEY, subkey_path)

                if subkey_name == "NonPackaged":
                    np_count, _, _ = winreg.QueryInfoKey(subkey)
                    for np_idx in range(np_count):
                        np_name = winreg.EnumKey(subkey, np_idx)
                        np_full_path = f"{WebcamDetect.WEBCAM_REG_SUBKEY}\\NonPackaged\\{np_name}"
                        np_key = winreg.OpenKey(WebcamDetect.REG_KEY, np_full_path)
                        if get_subkey_timestamp(np_key) == 0:
                            exe_name = self._get_exe_name(np_name)
                            pids = self._get_pids_by_name(exe_name)
                            active_apps.append((np_name, pids))
                        winreg.CloseKey(np_key)
                else:
                    if get_subkey_timestamp(subkey) == 0:
                        exe_name = self._get_exe_name(subkey_name)
                        pids = self._get_pids_by_name(exe_name)
                        active_apps.append((subkey_name, pids))
                winreg.CloseKey(subkey)
            winreg.CloseKey(key)
        except OSError:
            pass
        return active_apps

    def isActive(self):
        return len(self.getActiveApps()) > 0
