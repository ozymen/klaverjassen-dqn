import numpy as np

class Dumb:
    def __init__(self, playername):
        self.playerName = playername
        return None

    def setRound(self, round):
        self.round = round

    def pick(self, cards, eligableCards, state):
        """Picks a random legal card"""

        return np.random.choice(eligableCards)
