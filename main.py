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
    clear()
    print(g.board.track)
    print(f'Remaining Racers: {g.board.racers_remaining}')
    print(f'Available Bets: {g.bets}')
    print(f"{g.players[g.current_player].name}'s turn.")
    print(f'Money: {g.players[g.current_player].money} , Active Bets: {g.players[g.current_player].bets}')


    move = input('Do you want to roll (r) or bet (b)? : ')

    match move:
        case 'r':
            g.roll()
        case 'b':
            racer = input('Enter the racer you want to bet on to win this leg : ').upper()
            if racer not in g.bets:
                clear()
                leg()
            g.place_bet(g.players[g.current_player], racer)

    
    _ = input('Press enter to go to next player')
    g.next_player()
    clear()

def endgame():
    clear()
    print('##############GAME OVER ' + g.board.track[-1][-1] + ' WINS!!######################')
    print(g.board.track)
    _ = input('')

def payout():
    clear()
    print(g.board.track)
    print(f'The winner of this leg is Racer {g.leg_leader()}')
    g.leg_payout()
    print('After paying out the bets for this Leg, here is the standings')
    for player in g.players:
        print(f'{player.name}: {player.money}')
    _ = input('Press Enter to start the next leg.')
    g.phase = 'leg'

def game_loop():
    
    while g.phase == 'leg':
        leg()
        game_loop()
        

    while g.phase == 'payout':
        payout()
        game_loop()

    while g.phase == 'endgame':
        endgame()

g = game.Game(['player1','player2'])
print('######## STARTING POSITIONS ########')
print(g.board.track)
game_loop()


