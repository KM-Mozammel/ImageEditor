import tkinter as tk


class AdjustmentPanel(tk.Frame):

    def __init__(
        self,
        master,
        brightness,
        contrast,
        saturation,
        on_change,
    ):
        super().__init__(master)

        self.pack(fill="x", padx=10, pady=5)

        self.create_slider(
            "Brightness",
            brightness,
            on_change,
        )

        self.create_slider(
            "Contrast",
            contrast,
            on_change,
        )

        self.create_slider(
            "Saturation",
            saturation,
            on_change,
        )

    def create_slider(
        self,
        text,
        variable,
        on_change,
    ):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=3)

        tk.Label(
            frame,
            text=text,
            width=12,
            anchor="w",
        ).pack(side="left")

        tk.Scale(
            frame,
            from_=-100,
            to=100,
            orient="horizontal",
            variable=variable,
            command=lambda *_: on_change(),
        ).pack(side="left", fill="x", expand=True)