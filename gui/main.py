import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import bcrypt
import os

CREDENTIALS_FILE = "credentials.txt"

# this function will use bcrypt to hash the user's passwords for more security
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

# this will save credentials to the credentials.txt file
def save_credentials(username: str, password: str, filename=CREDENTIALS_FILE):
    hashed_pw = hash_password(password)
    with open(filename, "a") as f:
        f.write(f"{username}:{hashed_pw}\n")

# this function will read the user input and see if it matches with the 
# noted credentials in the credentials.txt file with the hash
def verify_credentials(username: str, password: str, filename=CREDENTIALS_FILE) -> bool:
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) != 2:
                    continue
                stored_user, stored_hash = parts
                if stored_user == username:
                    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                        return True
    except FileNotFoundError:
        return False
    return False

# ---this is the major page that first opens.
# it contains the login and sign up fields 
# uses tkinter elements to hold the fields in place
# may be updated
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgray")
        self.controller = controller

        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form_frame, text="Login", font=controller.title_font, bg="white").pack(pady=20)
        tk.Label(form_frame, text="Username", bg="white").pack()
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.pack()
        tk.Label(form_frame, text="Password", bg="white").pack()
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.pack()

        tk.Button(form_frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(form_frame, text="Sign Up",
                  command=lambda: controller.show_frame("SignUpPage")).pack()

        form_frame.tkraise()

    # check if the credentials are right, if true, go to page one
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if verify_credentials(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.controller.show_frame("StartPage")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

# this is the sign up page.
# contains user and password field

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgray")
        self.controller = controller

        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form_frame, text="Sign Up", font=controller.title_font, bg="white").pack(pady=20)
        tk.Label(form_frame, text="Username", bg="white").pack()
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.pack()
        tk.Label(form_frame, text="Password", bg="white").pack()
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.pack()

        tk.Button(form_frame, text="Register", command=self.register).pack(pady=10)
        tk.Button(form_frame, text="Back to Login",
                  command=lambda: controller.show_frame("LoginPage")).pack()

        form_frame.tkraise()

# this will use the save_credentials to write to the xredentials.txt file
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            save_credentials(username, password)
            messagebox.showinfo("Success", "Account created!")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

# when login is successful
# bring up the Start Page which gives user option for encryption page or decryption page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgray")
        self.controller = controller

        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form_frame, text="Choose an Option", font=controller.title_font, bg="white").pack(pady=20)
        tk.Button(form_frame, text="Go to Encrypt Page",
                  command=lambda: controller.show_frame("EncryptPage")).pack(pady=10)
        tk.Button(form_frame, text="Go to Decrypt Page",
                  command=lambda: controller.show_frame("DecryptPage")).pack(pady=10)
        tk.Button(form_frame, text="Logout",
                  command=lambda: controller.show_frame("LoginPage")).pack(pady=10)

        form_frame.tkraise()


class EncryptPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_file = None
        self.preview_photo = None

        self.original_bg = Image.open("assets/medicrypt_HQ.png")
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self.resize_bg)

        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form_frame, text="Encrypt Page", font=("Helvetica", 20), bg="white").pack(pady=10)
        tk.Button(form_frame, text="Go to Start Page",
                  command=lambda: controller.show_frame("StartPage")).pack(pady=5)
        tk.Button(form_frame, text="Import File", command=self.import_file).pack(pady=5)
        self.selected_label = tk.Label(form_frame, text="", bg="gray")
        self.selected_label.pack()
        self.image_preview = tk.Label(form_frame)
        self.image_preview.pack(pady=10)
        tk.Button(form_frame, text="Encrypt File", command=self.encrypt_file).pack(pady=5)
        self.file_label = tk.Label(form_frame, text="", bg="gray")
        self.file_label.pack()
        tk.Button(form_frame, text="Back to Start Page",
                  command=lambda: controller.show_frame("StartPage")).pack(pady=5)

        form_frame.tkraise()

    def resize_bg(self, event):
        resized = self.original_bg.resize((event.width, event.height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_photo)

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

        encrypted_data = fernet.encrypt(data)
        encrypted_file = self.selected_file + ".encrypted"
        with open(encrypted_file, "wb") as file:
            file.write(encrypted_data)

        key_file = os.path.splitext(self.selected_file)[0] + "_key.key"
        with open(key_file, "wb") as file:
            file.write(key)

        self.file_label.config(text=f"File encrypted: {encrypted_file}")
        messagebox.showinfo("Success",
                            f"Encrypted file saved as {encrypted_file}\nKey saved as {key_file}")


class DecryptPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_encrypted_file = None
        self.selected_key_file = None
        self.decrypted_filename = None

        self.original_bg = Image.open("assets/medicrypt_HQ.png")
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self.resize_bg)

        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form_frame, text="Decrypt Page", font=("Helvetica", 20), bg="white").pack(pady=10)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Medicrypt")
        self.geometry("1000x1000")
        self.title_font = ("Helvetica", 18)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # IMPORTANT for pages to expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        from page_one import EncryptPage
        from page_two import DecryptPage

        pages = (LoginPage, SignUpPage, StartPage, EncryptPage, DecryptPage)

        for Page in pages:
            frame = Page(parent=container, controller=self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
