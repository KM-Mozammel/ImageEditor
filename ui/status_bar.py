import tkinter as tk


class StatusBar(tk.Frame):
    """
    Bottom status bar.

    Examples:
    - Ready
    - Loading...
    - Saved
    - Zoom: 100%
    """

    def __init__(self, master):
        super().__init__(master)

        self.label = tk.Label(
            self,
            text="Ready",
            anchor="w",
        )

        self.label.pack(fill="x")

    def set_text(self, text):
        self.label.config(text=text)