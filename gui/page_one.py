import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os

# this class will create the structure of the GUI for this page
class EncryptPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_file = None
        self.preview_photo = None

        # Background
        # have it resize when the user makes it bigger or smaller
        self.original_bg = Image.open("assets/medicrypt_HQ.png")
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self.resize_bg)

        # Centered form
        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # this is a test label to keep track of what page is showing
        # may be removed later
        tk.Label(form_frame, text="Encrypt Page", font=("Helvetica", 20), bg="white").pack(pady=10)
        tk.Button(form_frame, text="Go to Start Page",
                  command=lambda: controller.show_frame("StartPage")).pack(pady=5)

        tk.Button(form_frame, text="Import File", command=self.import_file).pack(pady=5)
        self.selected_label = tk.Label(form_frame, text="", bg="gray")
        self.selected_label.pack()

        # show image preview in the GUI frame
        self.image_preview = tk.Label(form_frame)
        self.image_preview.pack(pady=10)

        # button for user to encrypt the selected file
        tk.Button(form_frame, text="Encrypt File", command=self.encrypt_file).pack(pady=5)
        self.file_label = tk.Label(form_frame, text="", bg="gray")
        self.file_label.pack()

        # brings them back to the selected menu
        tk.Button(form_frame, text="Back to Start Page",
                  command=lambda: controller.show_frame("StartPage")).pack(pady=5)

    # function to resize background image when window is resized
    def resize_bg(self, event):
        resized = self.original_bg.resize((event.width, event.height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_photo)

    # function to import file and show preview
    def import_file(self):
        filename = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*")])
        if filename:
            self.selected_file = filename
            self.selected_label.config(text=f"Selected file: {filename}")
            try:
                if filename.endswith(".encrypted"):
                    selected_image = Image.open("assets/nopreview.png").resize((400, 300), Image.LANCZOS)
                else:
                    selected_image = Image.open(filename).resize((400, 300), Image.LANCZOS)
                self.preview_photo = ImageTk.PhotoImage(selected_image)
                self.image_preview.config(image=self.preview_photo)
            except Exception:
                self.image_preview.config(image="", text="No preview available")

    def encrypt_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        key = Fernet.generate_key()
        fernet = Fernet(key)

        with open(self.selected_file, "rb") as file:
            data = file.read()

        # when the file is encrypted, save it as .encrypted
        encrypted_data = fernet.encrypt(data)
        encrypted_file = self.selected_file + ".encrypted"
        with open(encrypted_file, "wb") as file:
            file.write(encrypted_data)

        # file key file will be saved as originalfilename_key.key
        key_file = os.path.splitext(self.selected_file)[0] + "_key.key"
        with open(key_file, "wb") as file:
            file.write(key)

        self.file_label.config(text=f"File encrypted: {encrypted_file}")
        messagebox.showinfo("Success",
                            f"Encrypted file saved as {encrypted_file}\nKey saved as {key_file}")



   # def decrypt_file(self):
    #    if not self.selected_file or not self.selected_file.endswith(".encrypted"):
         #   messagebox.showerror("Error", "No encrypted file selected!")
          
          #  return

        #key_file = filedialog.askopenfilename(title="Select key file", filetypes=[("Key Files", "*.key")])
        #if not key_file:
         #   return

        #with open(key_file, "rb") as file:
         #   key = file.read()

        #fernet = Fernet(key)
       # with open(self.selected_file, "rb") as file:
        #    encrypted_data = file.read()

       # try:
        #    decrypted_data = fernet.decrypt(encrypted_data)
         #   decrypted_file = self.selected_file.replace(".encrypted", "")
          #  with open(decrypted_file, "wb") as file:
           #     file.write(decrypted_data)
           # self.file_label.config(text=f"File decrypted: {decrypted_file}")
           # messagebox.showinfo("Success", f"Decrypted file saved as {decrypted_file}")
        # except Exception as e:
          #  messagebox.showerror("Error", f"Decryption failed: {e}")
