from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("key.vault", "wb") as f:
    f.write(key)

print("[+] key.vault created successfully!")