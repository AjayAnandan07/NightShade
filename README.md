# NightShade: Encrypted C2 Framework for Security Research

NightShade is a proof-of-concept Command and Control (C2) architecture developed to study secure communication protocols, persistence mechanisms, and operational security (OpSec) in a networked environment.

## 🛡️ Core Features
- **Symmetric Encryption:** Utilizes AES-128 (Fernet) to secure the communication tunnel, ensuring data integrity and confidentiality.
- **Asynchronous Command Execution:** A multi-threaded Flask server handles concurrent agent check-ins and operator commands.
- **Advanced OpSec:** - **Jitter:** Randomized check-in intervals (10-25s) to evade pattern-based network detection.
  - **Windowless Execution:** The agent operates in the background without a GUI footprint.
- **Standalone Binary:** Compiled into a single `.exe` using PyInstaller with an embedded master key for zero-dependency deployment.

## 📂 Project Structure
- `server.py`: The command center. Handles decryption and result logging.
- `agent.pyw`: The background agent. Executes commands and scrambles output.
- `install.py`: Persistence script for automatic startup on Windows systems.

## 🚀 Usage (For Research Only)
1. Start the server: `python server.py`
2. Deploy the agent: Run `agent.exe` on the target machine.
3. Use the CLI on the server to interact with the connected agent.

*Disclaimer: This project is for educational purposes only. Unauthorized use on systems you do not own is strictly prohibited.*