import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import platform

# Encryption Key (MUST BE THE SAME ON BOTH PEERS)
KEY = b"1234567890123456"  # 16-byte key

def play_notification():
    """Plays a notification sound."""
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 100)
        else:
            from playsound import playsound
            playsound("\System\Library\Sounds\Ping.aiff")
    except Exception as e:
        print("Sound error:", e)

def pad_message(message):
    """Pads message to be a multiple of 16 bytes."""
    return message + " " * (16 - len(message) % 16)

def encrypt_message(message):
    """Encrypts the message using AES CBC mode."""
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(pad_message(message).encode()) + encryptor.finalize()
    return iv + encrypted_message  # Send IV + encrypted message

def decrypt_message(encrypted_message):
    """Decrypts the message using AES CBC mode."""
    iv = encrypted_message[:16]
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode().strip()

class P2PChat:
    def __init__(self, root, my_port, peer_ip, peer_port):
        self.root = root
        self.root.title("Secure P2P Chat")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.text_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.entry_message = tk.Entry(root, width=40)
        self.entry_message.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", my_port))

        self.peer_ip = peer_ip
        self.peer_port = peer_port

        # Start a separate thread to listen for messages
        self.listen_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.listen_thread.start()

    def send_message(self):
        message = self.entry_message.get()
        if message:
            encrypted_message = encrypt_message(message)
            self.sock.sendto(encrypted_message, (self.peer_ip, self.peer_port))
            self.display_message(f"You: {message}")
            self.entry_message.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                encrypted_message, _ = self.sock.recvfrom(1024)
                message = decrypt_message(encrypted_message)
                self.display_message(f"Peer: {message}")
            except Exception as e:
                print("Error receiving message:", e)

    def log_message(self, message):
        """Logs messages to a text file."""
        with open("chat_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")

    def display_message(self, message):
        """Displays and logs messages."""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)
        self.log_message(message)  # Save to file

if __name__ == "__main__":
    my_port = int(input("Enter your listening port: "))
    peer_ip = input("Enter peer's IP: ")
    peer_port = int(input("Enter peer's port: "))

    root = tk.Tk()
    chat_app = P2PChat(root, my_port, peer_ip, peer_port)
    root.mainloop()
