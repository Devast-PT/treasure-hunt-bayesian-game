import os
from tkinter import ttk, PhotoImage
import tkinter as tk

from modules.GameData import GameData


class Action(ttk.Button):
    """
    A custom button widget that switches between two modes: 'Detect' and 'Dig'.
    It changes appearance and behavior based on the mode.
    """
    image: dict

    def __init__(self, parent):
        """
        Initializes the Action button with parent widget.
        """
        self.parent = parent
        self.modeString = tk.StringVar(value="Mode: Detect")
        self._img_loader() # Load Images for the button

        super().__init__(master = parent)
        self._setup_ui() # Setup Styles for the button
        self.create_widgets() # Create and Configure


    @staticmethod
    def _setup_ui():
        """
        Defines custom styles for the button in Detect and Dig modes.
        """
        style = ttk.Style()
        # Style for 'Detect'
        style.configure(style='Search.Action.TButton',
                        background="lightgreen",
                        relief="solid",
                        borderwidth=2, bordercolor="aqua",
                        padding=5,
                        )

        # Style for 'Dig'
        style.configure(style='Dig.Action.TButton',
                        background="coral",
                        relief="solid",
                        borderwidth=2, bordercolor="aqua",
                        padding=5
                        )

        style.map('Search.Action.TButton', background=[('active', 'green')])
        style.map('Dig.Action.TButton', background=[('active', 'red')])


    def create_widgets(self):
        """
        Configures the button widget and binds additional events.
        """
        self.configure(image=self.image['search'],
                       compound = tk.LEFT,
                       textvariable=self.modeString,
                       command = self.mode_changer_event,
                       padding = 5,
                       style='Search.Action.TButton')
        self.master.bind_all("<Button-3>", self.mode_changer_event_right)

    def _img_loader(self):
        """
        Loads images for the button from the assets folder.
        """
        self.image = {
            'search': PhotoImage(file=r'assets/search.png'),
            'treasure': PhotoImage(file=r'assets/shovel.png')
        }
        print(os.listdir(r'assets/'))

    def mode_changer_event(self):
        """
        Event handler for left-clicks. Toggles the mode.
        """
        self._toggle_mode()

    def mode_changer_event_right(self, event):
        """
        Event handler for right-clicks. Toggles the mode.
        This method also receives the event argument from the bind.
        """
        self._toggle_mode()

    def _toggle_mode(self):
        """
        Toggles the current mode between 'Detect' and 'Dig', updates the button appearance,
        and modifies the GameData state.
        """
        if GameData.isDetectModeOn():
            self.modeString.set("Mode: Dig")
            self.config(image=self.image['treasure'], style='Dig.Action.TButton')
        else:
            self.modeString.set("Mode: Detect")
            self.config(image=self.image['search'], style='Search.Action.TButton')
        GameData.changeMode()

