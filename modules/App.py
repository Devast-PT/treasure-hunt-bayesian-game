import os
import sys
import tkinter as tk
from tkinter import ttk

from modules.Config import Config
from modules.GameArea import GameArea
from modules.GameData import GameData
from modules.MenuBar import MenuBar

class App(tk.Tk):
    """
    App serves as the main application window for the graphical interface.

    This class extends the base functionality of tkinter.Tk to create and manage
    a structured application layout with a menu bar and game area. It leverages
    customizable configurations through a config instance and themes provided by
    ttk. The application also provides the ability to restart programmatically.
    """
    menubar: MenuBar
    gamebar: GameArea

    def __init__(self):
        super().__init__()
        self.config = Config()
        GameData.initialize()
        self.setup_ui()
        self.create_widgets()
        self.create_layout()

    def setup_ui(self):
        current_theme = 'clam'

        self.title(self.config.title)
        self.resizable(False, False)

        style = ttk.Style()
        style.theme_use(current_theme)
        style.configure('.', font=(self.config.font_overall[0], self.config.font_overall[1]), background="black")

        print(f"Configurable options for 'TFrame': {style.configure('TWidget')}")

    def create_widgets(self):
        self.menubar = MenuBar(parent=self)
        self.gamebar = GameArea(parent=self)

    def create_layout(self):
        self.menubar.pack(side='left', fill='both')
        self.gamebar.pack(side='left', fill='both', expand=True)


    def run(self):
        self.mainloop()

    def restart(self):
        self.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)