import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from modules.BayesianNetwork import BayesianNetwork
from modules.GameData import GameData


class GameArea(ttk.Frame):
    """
    GameArea is a graphical interface component that represents the game area
    in a treasure-hunting game. It allows users to interact with a grid of
    buttons, reflecting Bayesian belief updates based on user actions.

    The class initializes and manages the user interface layout, button styles,
    and game interactions. It integrates with a Bayesian network to update
    beliefs and visually represent the game's state as the player makes
    selections or decisions.

    :ivar bayesnetwork: Instance of `BayesianNetwork` for managing game states
        and generating evidence based on the user's actions.
    :type bayesnetwork: BayesianNetwork
    :ivar button_grid: A dictionary mapping button positions (tuple of row and
        column) to ttk Button instances in the game grid.
    :type button_grid: dict
    :ivar clicked: List of strings representing grid positions that the user has
        already interacted with.
    :type clicked: list
    """
    def __init__(self, parent):
        super().__init__(master = parent)
        self.bayesnetwork = BayesianNetwork()
        self.button_grid = {}
        self.clicked = []

        self.setup_ui()
        self.create_widgets()
        self.create_layout()


    def setup_ui(self):
        for rc in range(GameData.rows):
            self.rowconfigure(rc, weight=1)
            self.columnconfigure(rc, weight=1)

        style = ttk.Style()

        style.configure("GameArea.TFrame", background="black",
                        relief="solid", borderwith=2, bordercolor="aqua",)

        # GameArea Buttons Initial
        style.configure('Initial.GameArea.TButton',
                        font=('Helvetica', 10, 'bold'),
                        relief="sunken", borderwidth=2, background="blue4",
                        bordercolor="aqua", foreground="white")

        style.map(
            'Initial.GameArea.TButton',
            foreground=[("active", "black")],
        )

        # GameArea button Signal +
        style.configure('S1.GameArea.TButton',
                        font=('Helvetica', 10, 'bold'),
                        relief="sunken", borderwidth=2, background="green",
                        bordercolor="aqua", foreground="black")

        # GameArea button Signal ++
        style.configure('S2.GameArea.TButton',
                        font=('Helvetica', 10, 'bold'),
                        relief="sunken", borderwidth=2, background="yellow",
                        bordercolor="aqua", foreground="black")

        # GameArea button Signal +++
        style.configure('S3.GameArea.TButton',
                        font=('Helvetica', 10, 'bold'),
                        relief="sunken", borderwidth=2, background="orange",
                        bordercolor="aqua", foreground="black")

        # GameArea button Signal ++++
        style.configure('S4.GameArea.TButton',
                        font=('Helvetica', 10, 'bold'),
                        relief="sunken", borderwidth=2, background="firebrick4",
                        bordercolor="aqua", foreground="white")

        # GameArea button Treasure Area
        style.configure('T.GameArea.TButton',
                        font=('Helvetica', 10, 'bold'),
                        relief="sunken", borderwidth=2, background="gold",
                        bordercolor="yellow", foreground="black")

    def create_widgets(self):
        belief = self.bayesnetwork.get_initial_belief()
        GameData.setBelief(belief)

        for pos, prob in GameData.getBelief().items():
            row , column = map(int, pos.strip("()").split(","))
            text = f"{prob:.4f}"
            button = ttk.Button(
                master = self,
                text=text,
                command= lambda r=row, c=column: self.detect_or_dig(r,c),
                style='Initial.GameArea.TButton'
            )
            self.button_grid[pos] = button

    def create_layout(self):
        for pos, button in self.button_grid.items():
            row , column = map(int, pos.strip("()").split(","))
            button.grid(row=row-1, column=column-1, ipady=5, sticky="nsew")
        self.configure(style="GameArea.TFrame")



    def detect_or_dig(self, row, column):
        """
        Handles the detection or digging mechanism in the game context, which allows players to
        either detect signals or dig for treasure depending on the current mode (`DetectMode` or
        `DigMode`).

        The method updates the game state based on the actions performed by the player. If in
        detect mode, it processes clicked tiles to reveal signals, update beliefs using a Bayesian
        network, and adjust probabilities. In dig mode, it confirms the player's intent, checks
        for treasure location, and determines if the game is won or lost. Additionally, it handles
        game conclusion if the player runs out of health points.

        :param row: The row index of the grid location being interacted with.
        :type row: int
        :param column: The column index of the grid location being interacted with.
        :type column: int
        :return: None
        """
        pos = f"({row},{column})"

        if GameData.isDetectModeOn():
            if pos not in self.clicked:
                self.clicked.append(pos)
                signal = self.bayesnetwork.evidenceGenerator(row, column) # Generate the new signal
                self.update_button(row, column, signal) # Update button colour based on signal
                GameData.setBelief(self.bayesnetwork.update_belief(GameData.getBelief())) # Updates Belief with prior
                GameData.damage() # Updated HP
                self.updateButtonsProbabilities() # Updated Grid Prob
            else:
                messagebox.showinfo(title="Sorry", message="Already clicked there.")
        else:
            pos = f"({row},{column})"
            text = f"Do you really want to dig in: {pos}"
            awner = messagebox.askquestion(title="Question", message=text)
            if awner == "yes":
                tpos = GameData.treasureLocation
                r, c = map(int, tpos.strip("()").split(","))
                self.button_grid[f"({r},{c})"].config(style="T.GameArea.TButton")
                if pos == tpos:
                    messagebox.showinfo(title="Congrats!", message=f"Congrats you found the TREASURE\n You won {int(GameData.currentHp)} Points!")
                else:
                    messagebox.showwarning(title="Sorry!", message=f"You failed to find the treasure located at {GameData.treasureLocation}")
                self.master.quit()

        if GameData.isPlayerDead():
            tpos = GameData.treasureLocation
            r, c = map(int, tpos.strip("()").split(","))
            self.button_grid[f"({r},{c})"].config(style="T.GameArea.TButton")
            messagebox.showwarning(title="0 HP!",
                                   message=f"You failed to find the treasure located at {GameData.treasureLocation}")
            self.master.quit()

    def updateButtonsProbabilities(self):
        for pos_renew, prob in GameData.getBelief().items():
            r, c = map(int, pos_renew.strip("()").split(","))
            self.button_grid[f"({r},{c})"].config(text=GameData.getProbText(prob))
        return

    def update_button(self, row, column, signal):
        match signal:
            case "+":
                signal = 1
            case "++":
                signal = 2
            case "+++":
                signal = 3
            case "++++":
                signal = 4
        self.button_grid[f"({row},{column})"].config(style=f"S{signal}.GameArea.TButton")









