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
    g.shuffle_racers() #equivalent to putting dice back into pyramid in tt game
    
    while len(g.board.racers) > 0:
        print(g.board.track)
        print(f'Availabl Bets: {g.bets}')
        print(f"{g.players[g.current_player].name}'s turn.")
        print(f'Money: {g.players[g.current_player].money} , Active Bets: {g.players[g.current_player].bets}')


        move = input('Do you want to roll (r) or bet (b)? : ')

        match move:
            case 'r':
                g.roll()
            case 'b':
                racer = input('Enter the racer you want to bet on to win this leg : ')
                g.place_bet(g.players[g.current_player], racer)

        
        _ = input('Press enter to go to next player')
        g.next_player()
        clear()

    if g.phase == 'end':
        print('##############GAME OVER ' + g.board.track[-1][-1] + ' WINS!!######################')
        print(g.board.track)
        _ = input('')
    else:
        print(g.board.track)
        print(f'The winner of this leg is Racer {g.leg_leader()}')
        g.leg_payout()
        print('After paying out the bets for this Leg, here is the standings')
        for player in g.players:
            print(f'{player.name}: {player.money}')
        _ = input('Press Enter to start the next leg.')
        leg()
    


g = game.Game(['player1','player2'])
print('######## STARTING POSITIONS ########')
print(g.board.track)
leg()


