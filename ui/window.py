import tkinter as tk
from tkinter import filedialog

from controllers.image_controller import ImageController

from ui.toolbar import Toolbar
from ui.adjustment_panel import AdjustmentPanel
from ui.image_canvas import ImageCanvas

class ImageEditor:

    def __init__(self):

        self.window = tk.Tk() #Tkinter root window তৈরি করে। শুধু memory-তে তৈরি হয়েছে। not in screen
        self.window.title("Image Editor") #Title set হয়।
        self.window.geometry("900x700") # Window size set হয়।

        self.controller = ImageController() # ImageController.__init__() run হবে।

        self.brightness_value = tk.IntVar(value=0) # brightness = 0
        self.contrast_value = tk.IntVar(value=0) # contrast = 0
        self.saturation_value = tk.IntVar(value=0) # saturation = 0

        self.create_widgets() # এখন UI তৈরি হবে।

        self.controller.load_image("assets/nature.jpg") # এই image load করো।
        self.canvas.display(self.controller.current_image)

    def create_widgets(self):

        self.toolbar = Toolbar(
            master=self.window,
            on_open=self.open_file,
            on_save=self.save_file,
            on_reset=self.reset_image,
            on_apply=self.apply_adjustments,
        )
        self.toolbar.pack(fill="x", pady=10)

        self.adjustment_panel = AdjustmentPanel(
            master=self.window,
            brightness=self.brightness_value,
            contrast=self.contrast_value,
            saturation=self.saturation_value,
            on_change=self.apply_adjustments,
        )

        self.canvas = ImageCanvas(self.window)
        
        #then return to __init__

    def apply_adjustments(self):

        self.controller.apply_adjustments(
            brightness=self.brightness_value.get(),
            contrast=self.contrast_value.get(),
            saturation=self.saturation_value.get(),
        )

        self.canvas.display(
            self.controller.current_image
        )

    def reset_controls(self):

        self.brightness_value.set(0)
        self.contrast_value.set(0)
        self.saturation_value.set(0)

    def reset_image(self):

        self.reset_controls()

        self.controller.reset()

        self.canvas.display(
            self.controller.current_image
        )

    def open_file(self):

        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
            ],
        )

        if not path:
            return

        self.controller.load_image(path)

        self.reset_controls()

        self.canvas.display(
            self.controller.current_image
        )

    def save_file(self):

        path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
            ],
        )

        if path:
            self.controller.save(path)

    def run(self):
        self.window.mainloop()