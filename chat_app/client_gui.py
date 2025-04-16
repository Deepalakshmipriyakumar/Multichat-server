import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# Server details
HOST = '127.0.0.1'
PORT = 12345

# Setup client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Prompt for username
name = simpledialog.askstring("Login", "Enter your name:")

# Function to receive messages
def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NAME':
                client.send(name.encode('utf-8'))
            else:
                chat.config(state='normal')
                chat.insert('end', msg + '\n')
                chat.yview('end')
                chat.config(state='disabled')

                # Save to log file
                with open("chat_log.txt", "a") as log_file:
                    log_file.write(msg + "\n")
        except:
            break

# Function to send message
def send_msg():
    text = entry.get().strip()
    if text:  # ✅ Only send if not empty
        message = f"{name}: {text}"
        client.send(message.encode('utf-8'))
        entry.delete(0, tk.END)
    else:
        print("⚠️ Empty message not sent.")

# GUI
win = tk.Tk()
win.title(f"Chat - {name}")
win.geometry("400x500")

chat = scrolledtext.ScrolledText(win, state='disabled')
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(win)
entry.pack(padx=10, pady=5, fill=tk.X)
entry.bind("<Return>", lambda e: send_msg())

send_btn = tk.Button(win, text="Send", command=send_msg)
send_btn.pack(pady=5)

# Start the receiver thread
threading.Thread(target=receive, daemon=True).start()

win.mainloop()
