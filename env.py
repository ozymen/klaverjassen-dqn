import math
import numpy as np
from player.dumb import Dumb as DumbPlayer
from player.simple import Simple as SimplePlayer

class KlaverjasGame:
    """ Game """
    def __init__(self, players, debug = False):
        self.debug = debug

        self.players = players

        self.suits = ['D', 'C', 'H', 'S']

        self.playerNames = ['n', 'e', 's', 'w']
        self.playerStart = 'n'

        self.teams = {'ns': ['n', 's'], 'ew': ['e', 'w']}


        self.cardPoints = {
            'trump': {'J': 20, '9': 14, 'A': 11, '1': 10, 'K': 4, 'Q': 3, '8': 0, '7': 0},
            'sans': {'A': 11, '1': 10, 'K': 4, 'Q': 3, 'J': 2, '9': 0, '8': 0, '7': 0}
        }

        self.cardRanking = {
            'trump': ['J', '9', 'A', '1', 'K', 'Q', '8', '7'],
            'sans': ['A', '1', 'K', 'Q', 'J', '9', '8', '7']
        }

    def startGame(self):
        print("New game is started")

        self.rounds = []
        self.points = {'ns': 0, 'ew': 0}

        playerstart = self.playerStart

        winner = None
        i = 0

        while winner is None:
            print("Round " + str(i) + " begins with " + playerstart)
            round = self.Round(self, playerstart)

            round.play()

            self.points['ns'] += round.points['ns']
            self.points['ew'] += round.points['ew']

            self.rounds.append(round)

            # set next player to start round
            playerstart = self.playerNames[(self.playerNames.index(playerstart) + 1) % 4]

            if self.points['ns'] > 1500 and self.points['ns'] != self.points['ew']:
                winner = 'ns'
            elif self.points['ew'] > 1500 and self.points['ew'] != self.points['ns']:
                winner = 'ew'

            i += 1

        print("Final: " + str(self.points))

        return True

    def getCardSuit(self, card):
        return int(math.floor(card/8))

    def getCardNumber(self, card):
        print(card % 8)
        return self.cardRanking['sans'][int(card % 8)]


    class Round:
        """  Round """

        def __init__(self, game, playerstart):
            self.tricks = []
            self.hands = {'n': [], 'e': [], 's': [], 'w': []}
            #self.playerStart = playerStart

            self.game = game

            self.highestbid = None
            self.playerstart = playerstart

        def play(self):

            while (self.highestbid is None):
                # shuffling and dealing cards
                self.deal()

                # bidding
                self.highestbid = {
                    'player': np.random.choice(self.game.playerNames),
                    'points': 80,
                    'trump': np.random.choice(self.game.suits)
                }

                self.highestbid = {
                    'player': 'n',
                    'points': 120,
                    'trump': np.random.choice(self.game.suits)
                }

                if self.highestbid['player'] in ['n', 's']:
                    self.highestbid['team'] = 'ns'
                else:
                    self.highestbid['team'] = 'ew'

            print("Highest bid of " + str(self.highestbid))

            # play tricks
            trickplayerstart = self.playerstart

            for i in range(8):
                trick = self.Trick(self.game, self, trickplayerstart)

                cards = trick.play()

                trickplayerstart = trick.winner

                self.tricks.append(trick)

            # scoring
            self.points = self.calculatePoints()

            return None



        def deal(self):

            r = np.random.choice(4*8, (4, 8), replace=False)

            self.hands['n'] = r[0].tolist()
            self.hands['e'] = r[1].tolist()
            self.hands['s'] = r[2].tolist()
            self.hands['w'] = r[3].tolist()

            return None

        def calculatePoints(self):

            points = {'ns': 0, 'ew': 0}
            finalpoints = {'ns': 0, 'ew': 0}

            if self.highestbid['trump'] is not 'sans':
                trumpindex = self.game.suits.index(self.highestbid['trump'])
            else:
                trumpindex = -1


            for trick in self.tricks:
                trickpoints = trick.getPoints()

                if trick.winner in self.game.teams['ns']:
                    points['ns'] += trickpoints
                else:
                    points['ew'] += trickpoints

            # check if score is higher or equal to bid
            if self.highestbid['team'] == 'ns':
                if points['ns'] >= self.highestbid['points']:
                    finalpoints['ns'] += points['ns']
                    finalpoints['ew'] += points['ew']
                else:
                    finalpoints['ew'] = points['ns']+points['ew']
            else:
                if points['ew'] >= self.highestbid['points']:
                    finalpoints['ew'] += points['ew']
                    finalpoints['ns'] += points['ns']
                else:
                    finalpoints['ns'] = points['ew']+points['ns']

            return finalpoints


        class Trick:
            """ Trick """
            def __init__(self, game, round, trickplayerstart):
                self.game = game
                self.round = round

                self.playerstart = trickplayerstart
                self.winner = None

            def play(self):
                self.cardsplayed = []
                player = self.playerstart

                print(self.round.hands)

                for i in range(4):
                    playercards = self.round.hands[player]
                    eligablecards = self.getEligableCards(playercards)

                    card = self.game.players[player].pick(playercards, eligablecards)

                    # remove card from hand
                    self.round.hands[player].remove(card)

                    player = self.game.playerNames[(self.game.playerNames.index(player)+1) % 4]

                    self.cardsplayed.append(card)

                self.winner = self.getWinner()

                return None

            def getEligableCards(self, playercards):
                # if this is the starting player, all cards are eligable
                if len(self.cardsplayed) == 0:
                    return playercards

                eligable = []
                highesttrump = 999

                suitasked = self.game.getCardSuit(self.cardsplayed[0])
                trumpsuit = self.game.suits.index(self.round.highestbid['trump'])

                # lets see if first card is trump
                if suitasked == trumpsuit:
                    trumpasked = True
                else:
                    trumpasked = False

                # array of eligable cards
                eligable = []

                if trumpasked:
                    trumpaskedranking = self.game.cardRanking['trump'].index(self.game.getCardNumber(self.cardsplayed[0]))

                    for card in playercards:
                        if self.game.getCardSuit(card) == suitasked:
                            trumpranking = self.game.cardRanking['trump'].index(self.game.getCardNumber(card))

                            if trumpranking < trumpaskedranking:
                                eligable.append(card)

                if len(eligable) == 0:
                    for card in playercards:
                        if self.game.getCardSuit(card) == suitasked:
                            eligable.append(card)

                # introeven and higher trump is asked if available
                if len(eligable) == 0:
                    # search for highest trump played
                    for cardplayed in self.cardsplayed:
                        if trumpsuit == self.game.getCardSuit(cardplayed):
                            trumpranking = self.game.cardRanking['trump'].index(self.game.getCardNumber(cardplayed))

                            if trumpranking < highesttrump:
                                highesttrump = trumpranking

                    # card needs to have higher trump rank value
                    for card in playercards:
                        if self.game.getCardSuit(card) == trumpsuit:
                            trumpranking = self.game.cardRanking['trump'].index(self.game.getCardNumber(card))

                            if trumpranking < highesttrump:
                                eligable.append(card)

                # if no card with suit asked and no (higher) trump is found, all card are eligable
                if len(eligable) == 0:
                    eligable = playercards

                return eligable

            def getWinner(self):
                """The winning player of the trick is calculated"""

                suitasked = self.game.getCardSuit(self.cardsplayed[0])
                trumpsuit = self.game.suits.index(self.round.highestbid['trump'])

                winner = None

                highesttrump = 999

                # check for trump
                for i, cardplayed in enumerate(self.cardsplayed):
                    if trumpsuit == self.game.getCardSuit(cardplayed):
                        trumpranking = self.game.cardRanking['trump'].index(self.game.getCardNumber(cardplayed))

                        if trumpranking < highesttrump:
                            highesttrump = trumpranking
                            winner = self.game.playerNames[(self.game.playerNames.index(self.playerstart) + i) % 4]

                # check for card of asked suit
                if winner is None:
                    # highestaskedsuit=self.game.cardRanking['sans'].index(self.game.getCardNumber(self.cardsplayed[0]))
                    highestaskedsuit = 999

                    for i, cardplayed in enumerate(self.cardsplayed):
                        if suitasked == self.game.getCardSuit(cardplayed):
                            suitranking = self.game.cardRanking['sans'].index(self.game.getCardNumber(cardplayed))

                            if suitranking < highestaskedsuit:
                                highestaskedsuit = suitranking
                                winner = self.game.playerNames[(self.game.playerNames.index(self.playerstart) + i) % 4]

                # otherwise, starting player is winner
                if winner is None:
                    winner = self.playerstart

                print("Cards " + str(self.cardsplayed))
                print("Winner " + winner)

                return winner

            def getPoints(self):
                points = 0

                trumpsuit = self.game.suits.index(self.round.highestbid['trump'])

                for cardplayed in self.cardsplayed:
                    if trumpsuit == self.game.getCardSuit(cardplayed):
                        points += self.game.cardPoints['trump'][self.game.getCardNumber(cardplayed)]
                    else:
                        points += self.game.cardPoints['sans'][self.game.getCardNumber(cardplayed)]

                return points



players = {'n': SimplePlayer('n'), 'e': DumbPlayer('e'), 's': SimplePlayer('s'), 'w': DumbPlayer('w')}

a = KlaverjasGame(players, True)

a.startGame()

