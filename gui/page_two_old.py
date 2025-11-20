import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os

class DecryptPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_encrypted_file = None
        self.selected_key_file = None
        self.decrypted_filename = None

        # Background
        bg_image = Image.open("assets/medicrypt_HQ.png").resize((800, 600), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Widgets
        tk.Label(self, text="Decrypt Page", font=("Helvetica", 20), bg="white").pack(pady=10)
        tk.Button(self, text="Go to Start Page", command=lambda: controller.show_frame("StartPage")).pack(pady=5)
        tk.Button(self, text="Import Encrypted File", command=self.import_encrypted_file).pack(pady=5)
        self.selected_label = tk.Label(self, text="", bg="gray")
        self.selected_label.pack()
        tk.Button(self, text="Import Key File", command=self.import_key_file).pack(pady=5)
        self.key_label = tk.Label(self, text="", bg="gray")
        self.key_label.pack()
        tk.Button(self, text="Decrypt", command=self.decrypt_and_display).pack(pady=5)
        self.decrypted_label = tk.Label(self, text="", bg="gray")
        self.decrypted_label.pack()
        self.image_label = tk.Label(self)
        self.image_label.pack()
        tk.Button(self, text="Download Image", command=self.download_image).pack(pady=5)

    def import_encrypted_file(self):
        filename = filedialog.askopenfilename(title="Select encrypted file", filetypes=[("Encrypted Files", "*.encrypted")])
        if filename:
            self.selected_encrypted_file = filename
            self.selected_label.config(text=f"Selected: {filename}")

    def import_key_file(self):
        filename = filedialog.askopenfilename(title="Select key file", filetypes=[("Key Files", "*.key")])
        if filename:
            self.selected_key_file = filename
            self.key_label.config(text=f"Selected key: {filename}")

    def decrypt_and_display(self):
        if not self.selected_encrypted_file or not self.selected_key_file:
            messagebox.showerror("Error", "Please select both encrypted file and key file.")
            return

        # Optional PIN check
        pin = simpledialog.askstring("PIN", "Enter your secret PIN:")
        if pin != "1234":  # Replace with real PIN logic
            messagebox.showerror("Error", "Incorrect PIN!")
            return

        decrypted_filename = self.decrypt_file(self.selected_encrypted_file, self.selected_key_file)
        if decrypted_filename:
            self.decrypted_label.config(text=f"Decrypted: {decrypted_filename}")
            decrypted_image = Image.open(decrypted_filename).resize((800, 600), Image.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(decrypted_image)
            self.image_label.config(image=self.preview_image)
            self.decrypted_filename = decrypted_filename
        else:
            messagebox.showerror("Error", "Decryption failed.")

    def decrypt_file(self, encrypted_file, key_file):
        try:
            with open(key_file, "rb") as f:
                key = f.read()
            with open(encrypted_file, "rb") as f:
                encrypted_data = f.read()
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_data)
            decrypted_filename = os.path.splitext(encrypted_file)[0] + "_decrypted.png"
            with open(decrypted_filename, "wb") as f:
                f.write(decrypted_data)
            return decrypted_filename
        except Exception as e:
            print(f"Error decrypting file: {e}")
            return None

    def download_image(self):
        if not self.decrypted_filename:
            messagebox.showwarning("Warning", "No decrypted file to save.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            try:
                with open(self.decrypted_filename, "rb") as src, open(save_path, "wb") as dest:
                    dest.write(src.read())
                messagebox.showinfo("Success", f"File saved as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
