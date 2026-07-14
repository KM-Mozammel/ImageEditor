import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from image_manager.loader import open_image
from image_manager.saver import save_image
from image_manager.state import ImageState

from numpy_processing.brightness import increase

class ImageEditor:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Editor")
        self.window.geometry("900x700")

        # Load Image
        self.state = ImageState()
        self.photo = None  
        
        self.create_widgets()

        self.load_image("assets/nature.jpg")

    def create_widgets(self):
        self.toolbar = tk.Frame(self.window)
        self.toolbar.pack(fill="x", pady=10)

        self.open_button = tk.Button(
            self.toolbar,
            text="Open",
            command=self.open_file
        )
        self.open_button.pack(side="left", padx=5)

        self.save_button = tk.Button(
            self.toolbar,
            text="Save",
            command=self.save_file
        )
        self.save_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(
            self.toolbar,
            text="Reset",
            command=self.reset_image
        )
        self.reset_button.pack(side="left", padx=5)

        self.edit_button = tk.Button(
            self.toolbar,
            text="Brightness",
            command=self.edit_image
        )
        self.edit_button.pack(side="left", padx=5)

        self.canvas = tk.Label(self.window)
        self.canvas.pack(pady=20)

    def load_image(self, path):

        image = open_image(path)
        self.state.original = image
        self.state.current = image.copy()
        self.show_image()

    def show_image(self):

        pil_image = Image.fromarray(
            self.state.current
        )
        
        pil_image.thumbnail((850, 600))

        self.photo = ImageTk.PhotoImage(pil_image)

        self.canvas.config(image=self.photo)

    def edit_image(self):

        self.state.current = increase(
            self.state.current,
            30
        )

        self.show_image()
        
    def reset_image(self):
        self.state.current = self.state.original.copy()
        self.show_image()
        
    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image Files",
                 "*.jpg *.jpeg *.png *.bmp")
            ]
        )
        
        if not path:
            return
        
        self.load_image(path)
        
    def save_file(self):
        path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp")
            ]

        )
        
        if not path:
            return
        
        save_image(
            self.state.current,
            path
        )
    
    def run(self):
        self.window.mainloop()