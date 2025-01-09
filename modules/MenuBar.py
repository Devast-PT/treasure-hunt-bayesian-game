import os
import sys
from tkinter import ttk, Button, Tk
import tkinter.font as font

from modules.widgets.Action import Action
from modules.widgets.HpBar import HpBar


class MenuBar(ttk.Frame):
    """
    MenuBar class defines a side menu with buttons and widgets for controlling the application.
    Includes a mode toggle button, an HP bar, and Restart/Quit buttons.
    """
    mode_button: Action
    hpbar: HpBar
    quit_restart_frame: ttk.Frame
    restart: ttk.Button
    quit: ttk.Button

    def __init__(self, parent):
        self._setup_ui()
        super().__init__(master = parent, padding='5', style='MenuBar.TFrame')
        self.create_widgets(parent)
        self.create_layout()

    @staticmethod
    def _setup_ui():
        style = ttk.Style()

        # MenuBar Frames
        style.configure('MenuBar.TFrame', background="black",
                        relief="solid", borderwidth=2, bordercolor="aqua",
                        padding=2)
        style.configure('QRFrame.MenuBar.TFrame', background="black",
                        borderwidth=0)

        # MenuBar Buttons
        style.configure('QRButton.MenuBar.TButton',
                        font=('Helvetica', 12, 'bold'),
                        relief="solid", borderwidth=2, background="blue4",
                        bordercolor="aqua", foreground="white")
        style.map(
            'QRButton.MenuBar.TButton',
            foreground=[("active", "black")],
        )


    def create_widgets(self, parent):
        self.mode_button = Action(self)
        self.hpbar = HpBar(self)

        self.quit_restart_frame = ttk.Frame(self, style='QRFrame.MenuBar.TFrame')
        self.restart = ttk.Button(self.quit_restart_frame, text="Restart",
                                  command=lambda: self.master.restart(),
                                  style="QRButton.MenuBar.TButton")
        self.quit = ttk.Button(self.quit_restart_frame, text="Quit",
                               command = lambda: parent.quit(),
                               style="QRButton.MenuBar.TButton")

    def create_layout(self):
        self.mode_button.pack(padx=20, pady=20)
        self.hpbar.pack(padx=20, pady=20, fill='y')
        self.restart.pack(side='left', padx=5)
        self.quit.pack(side='left', padx=5)
        self.quit_restart_frame.pack(pady=10)

