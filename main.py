import random
import game
import os
from rich import print
import inflect

p = inflect.engine()

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def leg():
    # clear screen and display updated game state info ie board/track, bets, predictions, etc
    clear()
    print(g.board.track)
    print(f'Remaining Racers: {g.board.racers_remaining}')
    print(f'Available Bets: {g.bets}')
    print(f'Winner Predictions : {g.prediction_winners}')
    print(f'Loser Predictions : {g.prediction_losers}')
    print(f"{g.players[g.current_player].name}'s turn.")
    print(f'Money: {g.players[g.current_player].money} , Active Bets: {g.players[g.current_player].bets}')

    # main turn loop. get player input and execute chosen move
    move = ''
    move = input('Do you want to roll (r), bet (b), or make prediction (p)? : ')

    match move:
        case 'r': # call game object roll method to move racers
            g.roll()

        case 'b': # take an available bet on winner of current leg
            racer = input('Enter the racer you want to bet on to win this leg : ').upper()
            while racer not in g.bets or len(g.bets[racer]) == 0:
                print('That racer is not available to bet on.')
                racer = input('Enter the racer you want to bet on to win this leg : ').upper()
            g.place_bet(g.players[g.current_player], racer)

        case 'p': # predict overall winner or loser for endgame bonuses
            prediction = input('Do you want to predict the overall winner (w) or loser (l)? : ')
            while prediction not in ['w','l']: 
                print('That is not a valid prediction.')
                prediction = input('Do you want to predict the overall winner (w) or loser (l)? : ')
            print(f'Racers available to predict: {g.players[g.current_player].predictions}')
            racer = input('Enter the racer you want to predict : ').upper()
            while racer not in g.players[g.current_player].predictions:
                print('That racer is not available to make a prediction on.')
                racer = input('Enter the racer you want to predict : ').upper()
            if prediction == 'w':
                g.predict_winner(g.players[g.current_player], racer)
            elif prediction == 'l':
                g.predict_loser(g.players[g.current_player], racer)
    
   # current player has made their move. display pass message, increment current player, and clear screen
    _ = input('Press enter to go to next player')
    g.next_player()
    clear()

def endgame():
    clear()
    print('##############GAME OVER ' + g.board.track[-1][-1] + ' WINS THE RACE!!!######################')
    print(g.board.track)
    g.prediction_payout()
    print('After paying out the bets and bonuses, here is the standings')
    # sort g.players by money and print with ordinal place
    for i, player in enumerate(sorted(g.players, key=lambda x: x.money, reverse=True)):
        print(f'{p.ordinal(i+1)} place : {player.name} with {player.money}')
    _ = input('Press enter to exit')

def payout():
    clear()
    print(g.board.track)
    g.leg_payout()
    print('After paying out the bets for this Leg, here is the standings')
    for i, player in enumerate(sorted(g.players, key=lambda x: x.money, reverse=True)):
        print(f'{p.ordinal(i+1)} place : {player.name} with {player.money}')
    _ = input('Press Enter to start the next leg.')
    g.phase = 'leg'

def game_loop():
    
    while g.phase == 'leg':
        leg()
        game_loop()
        
    # only way to leave phase 'leg' is by rolling the die of the last racer. so Game.roll handles phase change
    # not sure if that's good design or not. maybe better to keep the phase changes in the ""state machine"" game loop?

    while g.phase == 'payout':
        payout()
        game_loop()

    # only time phase gets changed to 'payout' is at the end of a leg. After a 'payout' phase is always a 'leg' phase.
    # For that reason game.leg_payout() handles phase change back to 'leg'

    while g.phase == 'endgame':
        endgame()

g = game.Game(['player1','player2'])
print('######## STARTING POSITIONS ########')
print(g.board.track)
game_loop()


