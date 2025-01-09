from tkinter import ttk

from modules.GameData import GameData

class HpBar(ttk.Frame):
    """
    HpBar is a graphical user interface (GUI) component that represents a health points (HP) bar in a vertical orientation.

    This class is designed to create, configure, and manage a custom HP progress bar using tkinter's ttk module.
    It provides a vertical progress indicator, along with labels displaying current points and the "Points" label.
    The purpose of this class is to visually represent a player's health points in real-time.

    :ivar progressbar: A ttk.Progressbar widget that visually indicates the current health points as a vertical bar.
    :type progressbar: ttk.Progressbar
    :ivar value_label: A ttk.Label widget displaying the numeric value of the health points.
    :type value_label: ttk.Label
    :ivar points_label: A ttk.Label widget displaying the text "Points" as an annotation to the bar.
    :type points_label: ttk.Label
    """
    progressbar: ttk.Progressbar
    value_label: ttk.Label
    points_label: ttk.Label

    def __init__(self, parent):
        super().__init__(parent, height = 50)

        self.hpbar_setup()
        self.create_widgets()
        self.create_layout()

    def hpbar_setup(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        style = ttk.Style()
        style.configure("TProgressbar", troughcolor="white", background="green", bordercolor="gray")
        style.configure("HpBar.TLabel", foreground="white")

    def create_widgets(self):
        self.progressbar = ttk.Progressbar(
            master=self,
            mode='determinate',
            orient='vertical',
            variable= GameData.getPointsVar(),
            length=150,
            style = 'TProgressbar'
        )

        self.value_label = ttk.Label(
            master=self,
            textvariable=GameData.getPointsVar(),
            font=("Helvetica", 16, "bold"),
            style="HpBar.TLabel"
        )

        self.points_label = ttk.Label(
            master=self,
            text="Points",
            font=("Helvetica", 16, "bold"),
            style="HpBar.TLabel"
        )

    def create_layout(self):
        self.progressbar.grid(row=0, column=0, sticky='nsew')
        self.value_label.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        self.points_label.grid(row=0, column=2, sticky='nsew')
