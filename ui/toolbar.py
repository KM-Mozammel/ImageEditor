import tkinter as tk


class Toolbar(tk.Frame):

    def __init__(
        self,
        master,
        on_open,
        on_save,
        on_reset,
        on_apply,
    ):
        super().__init__(master)

        tk.Button(
            self,
            text="Open",
            command=on_open,
        ).pack(side="left", padx=5)

        tk.Button(
            self,
            text="Save",
            command=on_save,
        ).pack(side="left", padx=5)

        tk.Button(
            self,
            text="Reset",
            command=on_reset,
        ).pack(side="left", padx=5)

        tk.Button(
            self,
            text="Apply",
            command=on_apply,
        ).pack(side="left", padx=5)