import random
import game
import os

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def leg():
    g.shuffle_racers()
    while len(g.board.racers) > 0:
        print(f"{g.players[g.current_player].name}'s turn.")
        print('racers left: ' + str(g.board.racers))
        g.roll()
        print(g.board.track)
        _ = input('')
        g.next_player()
        clear()

    if g.phase == 'end':
        print('Game Over')
        _ = input('')
    else:
        print('This is where the end of leg payouts happen')
        _ = input('')
        leg()
    


g = game.Game(['player1','player2'])
print('######## STARTING POSITIONS ########')
print(g.board.track)
leg()



# b1 = game.Board()
# print('#####STARTING POSITIONS########')
# print(b1.track)
# print('###############################')
# for i in range(15):
#     b1.roll()
#     print(b1.track)
#     print('racers left: ' + str(b1.racers))
#     x = input('next turn')
#     clear()

