import random
import tkinter as tk

from modules.Config import Config


class GameData:
    pointsVar: tk.IntVar
    mode: str
    treasureLocation: str
    belief: dict

    @classmethod
    def initialize(cls):
        cls.pointsVar = tk.IntVar(value=100)
        cls.mode = "Detect"
        data = Config.static_gamedata()
        cls.columns = data['columns']
        cls.rows = data['rows']
        cls.currentHp = 100
        cls.pointDmg = cls.currentHp / (cls.rows * cls.columns)
        cls.game = {}
        x, y = random.randint(1, cls.rows), random.randint(1, cls.columns)
        cls.treasureLocation = f"({x},{y})"
        print(f"Treasure in: {cls.treasureLocation}")

        cls.totalLocations = cls.rows * cls.columns
        for row in range(cls.rows):
            for col in range(cls.columns):
                cls.game[f"T({row},{col})"] = {
                    'initial_prob': 1/cls.totalLocations,
                    'signal': None,
                }

    @classmethod
    def getPointsVar(cls):
        return cls.pointsVar

    @classmethod
    def damage(cls):
        cls.currentHp -= cls.pointDmg
        cls.pointsVar.set(int(cls.currentHp))

    @classmethod
    def isDetectModeOn(cls):
        return cls.mode == "Detect"

    @classmethod
    def changeMode(cls):
        if cls.mode == "Detect":
            cls.mode = "Dig"
        else:
            cls.mode = "Detect"

    @classmethod
    def setBelief(cls, newBelief):
        cls.belief = newBelief

    @classmethod
    def getBelief(cls):
        return cls.belief

    @classmethod
    def isPlayerDead(cls):
        return cls.currentHp <= 0

    @staticmethod
    def getProbText(prob):
        return f"{prob:.4f}"