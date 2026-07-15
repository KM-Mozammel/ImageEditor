import tkinter as tk

from PIL import Image, ImageTk


class ImageCanvas(tk.Label):

    def __init__(self, master):
        super().__init__(master)

        self.photo = None

        self.pack(pady=20)

    def display(self, image):

        if image is None:
            return

        pil_image = Image.fromarray(
            image.astype("uint8")
        )

        pil_image.thumbnail((850, 600))

        self.photo = ImageTk.PhotoImage(pil_image)

        self.config(image=self.photo)