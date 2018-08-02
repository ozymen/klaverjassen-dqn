from env import KlaverjasGame
from player.dumb import Dumb as DumbPlayer
from player.mcts import Mcts
#from player.deepq import DeepQ



players = {'n': Mcts('n'), 'e': DumbPlayer('e'), 's': Mcts('s'), 'w': DumbPlayer('w')}

a = KlaverjasGame(players, True)

won = {'ns': 0, 'ew': 0}

for i in range(250):
    a.startGame()

    f = open('data/mcts5.csv', 'a+')

    f.write(str(a.points['ns']) + ',' + str(a.points['ew']) + "\n")

    f.close()

    if a.points['ns'] > a.points['ew']:
        won['ns'] += 1
    else:
        won['ew'] += 1


print(str(won))

