from env import KlaverjasGame
from player.dumb import Dumb as DumbPlayer


players = {'n': DumbPlayer('n'), 'e': DumbPlayer('e'), 's': DumbPlayer('s'), 'w': DumbPlayer('w')}

a = KlaverjasGame(players, True)

won = {'ns': 0, 'ew': 0}

for i in range(1000):
    a.startGame()

    if a.points['ns'] > a.points['ew']:
        won['ns'] += 1
    else:
        won['ew'] += 1


print(str(won))

