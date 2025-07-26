# 🧠 Keylogger Control Panel GUI

This is a Python-based GUI tool that allows you to:

* Generate a keylogger EXE file that silently logs keystrokes and sends encrypted logs to your system
* Receive and decrypt keylogs from the remote sender using a professional GUI interface

---

## 🚀 Features

* 🔐 Fernet-encrypted keylog transmission
* 🖥️ GUI for generating EXE and receiving logs
* 🛠 Built-in EXE generator (using `pyinstaller`)
* 🔢 Same secret key used for both sender and receiver
* 📋 Save decrypted logs as a text file

---

## 📁 Folder Structure

```
keylogger-control-gui/
├── receiver_gui.py         # GUI interface (main file)
├── single_run.pyw          # Keylogger sender script template
├── dist/                   # Folder where EXE gets created
└── README.md               # This file
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

Required packages:

* tkinter (comes built-in)
* cryptography
* pyinstaller (for generating EXE)

---

## ▶️ Run the App

**Option 1: Run from Python source**

```
Just double-click:
src/receiver_gui.py
```

**Option 2: Build Windows EXE**

```bash
pyinstaller --noconsole --onefile receiver_gui.py
```

⚠️ **Note:**
Antivirus may block the EXE (due to keylogging behavior)

Tool is for learning and authorized use only.

---

## 📄 License

Licensed under the MIT License
See `LICENSE` for full terms.

---

## 👤 Author

**Mahavir Harijan**
GitHub: [@Mahavirharijan](https://github.com/Mahavirharijan)
