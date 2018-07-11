import numpy as np

class Dumb:
    def __init__(self, playername):
        self.playerName = playername
        return None

    def pick(self, cards, eligableCards):
        """Picks a random legal card"""

        return np.random.choice(eligableCards)
