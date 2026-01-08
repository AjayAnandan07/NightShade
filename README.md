🌑 NightShade Framework v4.0
NightShade is a lightweight, encrypted Command & Control (C2) framework developed for educational security research. It demonstrates the lifecycle of a modern security threat, from initial check-in and persistence to automated data exfiltration and self-sanitization.

🚀 Key Features

Encrypted Tunneling: Communication is secured using AES-128 bit (Fernet) symmetric encryption to prevent traffic inspection.



Persistent Execution: Includes a Windows Registry persistence module to survive system reboots.



Stealth & Evasion: Features integrated Anti-Sandbox detection (RAM/CPU/Process checks) to avoid execution in analysis environments.


Asynchronous Intel: Background multi-threaded Keylogger and Screengrab modules for continuous data collection.




Automated Mission Control: A real-time Flask Web Dashboard with an infinite automation loop for hands-free exfiltration.



Clean Exit: A dedicated self_destruct module to wipe forensic footprints and registry keys upon mission completion.

🛠️ Technical Stack
Language: Python 3.x


Backend: Flask (Web C2 Server) 



Security: Cryptography (Fernet AES) 


Libraries: mss (Screengrab), pynput (Keylogging), psutil (System Monitoring) 



📅 Development Journey
This project was developed during a 30-day intensive cybersecurity learning journey (Dec 2025 - Jan 2026).


Phase 1: Core C2 Bridge & Multi-threading 


Phase 2: Encryption & Stealth Binaries 


Phase 3: Exfiltration & Persistence 



Phase 4: Web UI Migration & Loop Automation 


⚖️ Legal Disclaimer
FOR EDUCATIONAL PURPOSES ONLY. This framework is intended for authorized security testing and research. Unauthorized use of this software against systems without prior explicit consent is strictly prohibited and may violate local and international laws. The author assumes no liability for misuse.
