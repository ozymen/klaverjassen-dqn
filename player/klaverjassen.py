import numpy as np
import math

class Klaverjassen:
    def __init__(self, history, playerName, playerPossibleCardsLeft):
        self.players = ['n', 'e', 's', 'w']

        self.history = history

        self.suits = ['D', 'C', 'H', 'S', 'N']

        self.cardPoints = {
            'trump': {'J': 20, '9': 14, 'A': 11, '1': 10, 'K': 4, 'Q': 3, '8': 0, '7': 0},
            'sans': {'A': 11, '1': 10, 'K': 4, 'Q': 3, 'J': 2, '9': 0, '8': 0, '7': 0}
        }

        self.cardRanking = {
            'trump': ['7', '8', 'Q', 'K', '1', 'A', '9', 'J'],
            'sans': ['7', '8', '9', 'J', 'Q', 'K', '1', 'A']
        }

        self.cardValues = ['A', '1', 'K', 'Q', 'J', '9', '8', '7']

        self.playerName = playerName
        self.playerIndex = self.players.index(playerName)

        self.playerPossibleCardsLeft = playerPossibleCardsLeft

    def current_player(self, state):


        begin = self.players.index(state[3][-1])


        begin += (len(state[2]) % 4)

        begin = begin % 4



        return self.players[begin]

    def legal_actions(self, history):

        state = history[-1]


        currentplayer = self.players.index(self.current_player(state))

        #print("LEGAL STATE")
        #print(state)

        if currentplayer == self.playerIndex:
            allcards = np.setdiff1d(state[1], state[2])

            cardsintricklen = len(state[2]) % 4

            if cardsintricklen > 0:
                cardsintrick = state[2][-cardsintricklen:]

                suitasked = math.floor(cardsintrick[0]/8)

                newallcards = []

                for card in allcards:
                    if math.floor(card/8) == suitasked:
                        newallcards.append(card)

                # trump needed
                if len(newallcards) == 0:
                    for card in allcards:
                        if math.floor(card / 8) == self.suits.index(state[0][2]):
                            newallcards.append(card)

                if len(newallcards) == 0:
                    newallcards = allcards

                allcards = np.array(newallcards)

            return allcards.tolist()
        else:
            # return all cards possible
            allcards = np.arange(32, dtype=np.int8)
            #print(state)

            hand = np.array(state[1], dtype=np.int8)
            cardsplayed = np.array(state[2], dtype=np.int8)


            if len(cardsplayed) > 0:
                #print(hand)
                #print(cardsplayed)
                hand = np.append(hand, cardsplayed)


            allcards = np.setdiff1d(allcards, hand)

            #allcards = np.intersect1d(allcards, self.playerPossibleCardsLeft[self.players[currentplayer]])

            return allcards.tolist()




    def next_state(self, state, action):

        tricks = np.array(state[2])

        action = int(action)

        tricks = np.append(tricks, action)
        tricks = np.array(tricks, dtype=np.int8)
        #print(state)
        trickwinners = np.array(state[3])
        #print(trickwinners)
        #print ("AA")

        if len(tricks) % 4 == 0:
            highestcardvalue = -1
            trickwinner = state[3][-1]
            player = state[3][-1]

            #print(state)
            #print(action)
            #print(tricks[-4:])

            for card in tricks[-4:]:


                cardsuit = int(math.floor(card/8))
                cardval = self.cardValues[int(card % 8)]

                if cardsuit == state[0][2]:
                    val = self.cardRanking['trump'].index(cardval)*10
                else:
                    val = self.cardRanking['sans'].index(cardval)

                if val > highestcardvalue:
                    highestcardvalue = val
                    trickwinner = player

                player = self.players[(self.players.index(player)+1) % 4]

            #print(highestcardvalue)
            #print(trickwinner)
            #print ("XXXXXXXXXXxx")
            #exit(0)

            #trickwinners = np.append(trickwinners, self.trickWinner(tricks[-4:], state[3][-1]))
            trickwinners = np.append(trickwinners, trickwinner)
            #print(trickwinners)



        tricks = tuple(tricks)
        trickwinners = tuple(trickwinners.tolist())
        #print(tricks)

        newstate = (state[0], state[1], tricks, trickwinners)
        #print(newstate)
        return newstate

    def unpack_action(self, action):
        return action

    def is_ended(self, history):
        state = history[-1]

        if len(state[2]) == 32:
            return True
        else:
            return False

    def win_values(self, history):

        # check whether bid has been achieved

        return {'n': 1, 'e': 0, 's': 1, 'w': 0}

    def points_values(self, history):
        state = history[-1]

        if len(state[2]) == 0:
            return {'n': 0, 'e': 0, 's': 0, 'w': 0}

        ns = 0
        ew = 0

        for i in range(math.floor(len(state[2])/4)):
            points = self.calculate_points(state[0][2], state[2][i*4:(i+1)*4], state[3][i+1])
            if state[3][i+1] in ['n', 's']:
                ns += points

                if i == 7:
                    ns += 10
            else:
                ew += points

                if i == 7:
                    ns += 10

        # check if trick is won by someone with highest card (no higher cards left in hands)

        return {'n': ns, 'e': ew, 's': ns, 'w': ew}



    def calculate_points(self, trump, trick, winner):
        points = 0

        for card in trick:
            if math.floor(card/8) == self.suits.index(trump):
                points += self.cardPoints['trump'][self.cardValues[card % 8]]
            else:
                points += self.cardPoints['sans'][self.cardValues[card % 8]]

        return points

