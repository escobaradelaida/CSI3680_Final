import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=600)
        self.controller = controller

        # Load the image using PIL
        self.bg_image = Image.open('../assets/medicrypt_HQ.png')
        self.bg_photo = controller.resize_image(self.bg_image, 800, 600)

        # Create a label to display the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create other widgets
        label = tk.Label(self, text='This is page one', font=controller.title_font, bg="white")
        label.pack(side='top', fill='x', pady=10)

        button = tk.Button(self, text='Go to the Start Page', command=lambda: controller.show_frame('StartPage'))
        button.pack()

        import_button = tk.Button(self, text = "Import File", command=self.import_file)
        import_button.pack()

        # create a display to show the user that their file has been selected
        self.selected_label = tk.Label(self, text="", bg="gray")
        self.selected_label.pack()

        # load the image that the user selected
        self.image_preview = tk.Label(self)
        self.image_preview.pack()

        # encrypt button
        encrypt_button = tk.Button(self, text="Encrypt File", command=self.encrypt_file)
        encrypt_button.pack()

        # displays the selected file
        self.file_label = tk.Label(self, text="", bg="gray")
        self.file_label.pack()

        # Ensure buttons and labels appear above the background
        label.lift()
        button.lift()
        import_button.lift()
        self.selected_label.lift()

    def import_file(self):
        filename = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*")])
        if filename:
            self.selected_file = filename
            self.selected_label.config(text=f"Selected file: {filename}")
            print("Selected file: ", filename)

            # show the user their selected image using PIL
            selected_image = Image.open(filename)
            resized_image = selected_image.resize((400, 300), Image.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(resized_image)

            # display the image
            self.image_preview.config(image=self.preview_photo)

    def encrypt_file(self):
        # creatte the encryption key
        if self.selected_file:
            # generate key
            key = Fernet.generate_key()
            cipher = Fernet(key)

            # read the selected file
            with open(self.selected_file, "rb") as file:
                file_content = file.read()

            # encrypt the file data
            encrypted_data = cipher.encrypt(file_content)

            # save encryted data to a new file
            encrypted_file = self.selected_file + ".encrypted" # i believe this is the suffix of the new file
            with open(encrypted_file, "wb") as file:
                file.write(encrypted_data)

            # show the user that the encryption was successful
            self.file_label.config(text=f"File encrypted and saved as {encrypted_file}")
            print("File encrypted and saved as: ", encrypted_file)

            # save encryption key to a file
            key_file = os.path.splitext(self.selected_file)[0] + "_key.key"
            with open(key_file, "wb") as file:
                file.write(key)

            print("Encrypted file saved as: ", key_file)
        else:
            self.file_label.config(text="File not selected")
            print("No File to Encrypt")

if __name__ == "__main__":
    root = tk.Tk()
    root.mainloop()