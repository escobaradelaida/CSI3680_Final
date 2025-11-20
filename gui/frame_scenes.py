import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from page_one import PageOne
from gui.page_two_old import PageTwo


class AppWindows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the size of the main window
        self.geometry("800x600")

        # Font for the title
        self.title_font = font.Font(family='Helvetica', size=18, weight='bold')

        # The container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Put all of the pages in the same location
            # The one on the top will be the visible one
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show the frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def resize_image(self, image, frame_width, frame_height):
        # Get the aspect ratios
        img_width, img_height = image.size
        img_aspect = img_width / img_height
        frame_aspect = frame_width / frame_height

        if img_aspect > frame_aspect:
            # Image is wider than the frame
            new_width = frame_width
            new_height = int(frame_width / img_aspect)
        else:
            # Image is taller than the frame
            new_height = frame_height
            new_width = int(frame_height * img_aspect)

        # Resize the image while maintaining the aspect ratio
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=600)
        self.controller = controller

        # Load the image using PIL
        self.bg_image = Image.open('./assets/medicrypt_HQ.png')
        self.bg_photo = controller.resize_image(self.bg_image, 800, 600)

        # Create a label to display the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # entry box
        self.entry = tk.Entry(self)
        self.entry.pack()

        # button that checks for logins???
        self.check_button = tk.Button(self, text="Check Value", command=self.check_value)
        self.check_button.pack()

        # error label
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

        # Create other widgets
        label = tk.Label(self, text='This is the start page', font=controller.title_font, bg="white")
        label.pack(side='top', fill='x', pady=10)

        button1 = tk.Button(self, text='Go to Encryption', command=lambda: controller.show_frame('PageOne'))
        button2 = tk.Button(self, text='Go to Decryption', command=lambda: controller.show_frame('PageTwo'))

        button1.pack()
        button2.pack()

        # Ensure buttons and labels appear above the background
        label.lift()
        button1.lift()
        button2.lift()
        self.check_button.lift()

    # allow the user to progress if they type correct credentials
    def check_value(self):
        value = self.entry.get().strip() # use strip to get the value from the entry field
        if value == "1234": # pretend this is the nurse's ID
            self.controller.show_frame('PageOne') # move them to pageone
            # make error label for user to see
            self.error_label.config(text="") # cleared if error message is not needed
        else:
            # if they put in the wrong creds, give error message
            self.error_label.config(text="Credentials are incorrect. Please try again.")



if __name__ == '__main__':
    app = AppWindows()
    app.mainloop()