import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from image_manager.loader import open_image
from image_manager.saver import save_image
from image_manager.state import ImageState

from numpy_processing.brightness import adjust_brightness, adjust_contrast, adjust_saturation


class ImageEditor:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Editor")
        self.window.geometry("900x700")

        self.state = ImageState()
        self.photo = None
        self.brightness_value = tk.IntVar(value=0)
        self.contrast_value = tk.IntVar(value=0)
        self.saturation_value = tk.IntVar(value=0)

        self.create_widgets()
        self.load_image("assets/nature.jpg")

    def create_widgets(self):
        self.toolbar = tk.Frame(self.window)
        self.toolbar.pack(fill="x", pady=10)

        self.open_button = tk.Button(self.toolbar, text="Open", command=self.open_file)
        self.open_button.pack(side="left", padx=5)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_file)
        self.save_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(self.toolbar, text="Reset", command=self.reset_image)
        self.reset_button.pack(side="left", padx=5)

        self.edit_button = tk.Button(self.toolbar, text="Apply", command=self.apply_adjustments)
        self.edit_button.pack(side="left", padx=5)

        self.controls_frame = tk.Frame(self.window)
        self.controls_frame.pack(fill="x", padx=10, pady=5)

        self._create_slider("Brightness", self.brightness_value)
        self._create_slider("Contrast", self.contrast_value)
        self._create_slider("Saturation", self.saturation_value)

        self.canvas = tk.Label(self.window)
        self.canvas.pack(pady=20)

    def _create_slider(self, label_text, variable):
        frame = tk.Frame(self.controls_frame)
        frame.pack(fill="x", pady=3)

        tk.Label(frame, text=label_text, width=12, anchor="w").pack(side="left")
        tk.Scale(
            frame,
            from_=-100,
            to=100,
            orient="horizontal",
            variable=variable,
            command=lambda *_: self.apply_adjustments(),
        ).pack(side="left", fill="x", expand=True)

    def load_image(self, path):
        image = open_image(path)
        self.state.original = image
        self.state.current = image.copy()
        self.reset_controls()
        self.show_image()

    def show_image(self):
        if self.state.current is None:
            return

        pil_image = Image.fromarray(self.state.current.astype("uint8"))
        pil_image.thumbnail((850, 600))

        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.config(image=self.photo)

    def apply_adjustments(self):
        if self.state.original is None:
            return

        image = self.state.original.copy()
        image = adjust_brightness(image, self.brightness_value.get())
        image = adjust_contrast(image, self.contrast_value.get())
        image = adjust_saturation(image, self.saturation_value.get())
        self.state.current = image
        self.show_image()

    def reset_controls(self):
        self.brightness_value.set(0)
        self.contrast_value.set(0)
        self.saturation_value.set(0)

    def reset_image(self):
        self.reset_controls()
        if self.state.original is not None:
            self.state.current = self.state.original.copy()
        self.show_image()

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")],
        )

        if not path:
            return

        self.load_image(path)

    def save_file(self):
        path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")],
        )

        if not path:
            return

        save_image(self.state.current, path)

    def run(self):
        self.window.mainloop()