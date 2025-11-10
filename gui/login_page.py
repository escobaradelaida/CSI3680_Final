import tkinter as tk
from tkinter import messagebox

# Function to check login credentials
def check_credentials(username, password):
    try:
        with open('credentials.txt', 'r') as file:
            credentials = file.readlines()
        for credential in credentials:
            stored_username, stored_password = credential.strip().split(',')
            if stored_username == username and stored_password == password:
                return True
        return False
    except FileNotFoundError:
        return False

# Function to handle login button click
def login():
    username = username_entry.get()
    password = password_entry.get()
    if check_credentials(username, password):
        messagebox.showinfo("Login Success", "Welcome!")
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

# Function to register new user
def register():
    registration_window = tk.Toplevel(root)
    registration_window.title("Register")

    def register_user():
        admin_key = admin_key_entry.get()
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()
        if admin_key == "admin_passkey":  # Replace "admin_passkey" with your actual admin passkey
            with open('credentials.txt', 'a') as file:
                file.write(f"{new_username},{new_password}\n")
            messagebox.showinfo("Registration Success", "User registered successfully!")
            registration_window.destroy()
        else:
            messagebox.showerror("Registration Failed", "Invalid admin passkey.")

    tk.Label(registration_window, text="Admin Passkey:").grid(row=0, column=0)
    admin_key_entry = tk.Entry(registration_window, show="*")
    admin_key_entry.grid(row=0, column=1)

    tk.Label(registration_window, text="New Username:").grid(row=1, column=0)
    new_username_entry = tk.Entry(registration_window)
    new_username_entry.grid(row=1, column=1)

    tk.Label(registration_window, text="New Password:").grid(row=2, column=0)
    new_password_entry = tk.Entry(registration_window, show="*")
    new_password_entry.grid(row=2, column=1)

    tk.Button(registration_window, text="Register", command=register_user).grid(row=3, column=1)

# Main application window
root = tk.Tk()
root.title("Login")

tk.Label(root, text="Username:").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

tk.Button(root, text="Login", command=login).grid(row=2, column=1)
tk.Button(root, text="Register", command=register).grid(row=3, column=1)

root.mainloop()