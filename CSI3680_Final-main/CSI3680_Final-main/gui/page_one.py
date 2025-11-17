import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os

# Function to import medical images
def import_file():
    global selected_file, preview_photo

    # Allow the user to supply a local file
    filename = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All Files", "*.*")]
    )

    # Check whether a file has been supplied
    if filename:
        selected_file = filename
        selected_label.config(text=f"Selected file: {filename}")
        print("Selected file:", filename)

        # Check whether the file supplied is already encrypted
        if filename.endswith(".encrypted"):
            # Can't display encrypted files using PIL
            # So just display an image letting the user know that no preview is available
            selected_image = Image.open("CSI3680_Final-main/assets/nopreview.jpg")
            resized_image = selected_image.resize((400, 300), Image.LANCZOS)
        
            # display the no preview image
            preview_photo = ImageTk.PhotoImage(resized_image)
            image_preview.config(image=preview_photo)

        else:
            # show the user their selected image using PIL
            selected_image = Image.open(filename)
            resized_image = selected_image.resize((400, 300), Image.LANCZOS)
        
            # display the image
            preview_photo = ImageTk.PhotoImage(resized_image)
            image_preview.config(image=preview_photo)

# Function to generate the symmetric encryption key using Fernet
def generate_key():
    # Generate key
    key = Fernet.generate_key()

    # Save the key to a file called filekey.key
    with open('filekey.key', 'wb') as file:
        file.write(key)

# Function to encrypt medical images supplied by the user
def encrypt_file():

    # Generate the symmetric key
    generate_key()

    global selected_file

    # Check whehter a file has been supplied
    if selected_file:
        # Load the key file
        with open('filekey.key', 'rb') as file:
            key = file.read()

        # Create an instance of Fernet using the key
        fernet = Fernet(key)

        # Save the unencrypted file supplied by the user
        with open(selected_file, 'rb') as file:
            unencrypted_file = file.read()

        # encrypt the file data
        encrypted_data = fernet.encrypt(unencrypted_file)

        # Save the encrypted file data to a new file
        encrypted_file = selected_file + ".encrypted"
        with open(encrypted_file, 'wb') as file:
            file.write(encrypted_data)

        # show the user that the encryption was successful
        file_label.config(text=f"File encrypted and saved as {encrypted_file}")
        print("File encrypted and saved as:", encrypted_file)

    else:
        file_label.config(text="File not selected")
        print("No file to Encrypt")

# Function to decrypt medical images supplied by the user
def decrypt_file():
    global selected_file

    # Check whether a file has been supplied
    if selected_file:
        # Load the key file
        with open('filekey.key', 'rb') as file:
            key = file.read()

        # Create an instance of Fernet using the key
        fernet = Fernet(key)

        # Save the encrypted file supplied by the user
        with open(selected_file, 'rb') as file:
            encrypted_file = file.read()

        # decrypt the file data
        decrypted_data = fernet.decrypt(encrypted_file)

        # Save the decrypted file data to a new file
        # selected_file.replace(".encrypted", "") removes the .encrypted extension on the original filename
        decrypted_file = selected_file.replace(".encrypted", "")
        with open(decrypted_file, 'wb') as file:
            file.write(decrypted_data)

        # show the user that the encryption was successful
        file_label.config(text=f"File decrypted and saved as {decrypted_file}")
        print("File decrypted and saved as:", decrypted_file)

    else:
        file_label.config(text="File not selected")
        print("No file to Decrypt")

# Create global variable that will store the image supplied by the user 
# so it can be easily accessed in the import_file(), encrypt_file(), and decrypt_file() functions
selected_file = None

root = tk.Tk()
root.title("Page One")

# Set window and backgroud image dimensions
width = 900
height = 900

bg_image = Image.open("CSI3680_Final-main/assets/medicrypt_HQ.png")

# Resize while keeping quality using LANCZOS
bg_image = bg_image.resize((width, height), Image.LANCZOS)

bg_photo = ImageTk.PhotoImage(bg_image)

# Set window to match resized image
root.geometry(f"{width}x{height}")

# Create a label to display the background image    
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create other widgets
label = tk.Label(root, text='This is page one', font=("Helvetica", 20), bg="white")
label.pack(side='top', fill='x', pady=10)

# start button
button = tk.Button(root, text='Go to the Start Page', command="")
button.pack()

# import button
import_button = tk.Button(root, text="Import File", command=import_file)
import_button.pack()

# create a display to show the user that their file has been selected
selected_label = tk.Label(root, text="", bg="gray")
selected_label.pack()

# load the image that the user selected
image_preview = tk.Label(root)
image_preview.pack()

# encrypt button
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_file)
encrypt_button.pack()

file_label = tk.Label(root, text="", bg="gray")
file_label.pack()

# decrypt button
decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_file)
decrypt_button.pack()

# Ensure buttons and labels appear above the background
label.lift()
button.lift()
import_button.lift()
encrypt_button.lift()
decrypt_button.lift()
selected_label.lift()

# Start the program
root.mainloop()