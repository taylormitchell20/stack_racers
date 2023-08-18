import random

class Game:
    def __init__(self, player_names) -> None:
        self.board = Board()
        self.current_player = 0
        self.players = []
        for player in player_names:
            p = Player(player)
            self.players.append(p)
        self.phase = 'leg' # might need to change to int
        self.bets = {'A': [5,3,2], 'B': [5,3,2], 'C': [5,3,2], 'D': [5,3,2], 'E': [5,3,2]}
        self.prediction_winners = []
        self.prediction_losers = []
        
    def prediction_payout(self):
        winner = self.get_leg_results(1)
        payouts = [8,5,3,2,1]
        print(f'Racer {winner} is the winner of the Race!')
        for player, prediction in self.prediction_winners:
            if prediction == winner:
                if payouts[0] == 1:
                    print(f'{player.name} earned 1 for predicting {prediction} would win!')
                    player.money += 1
                else:
                    print(f'{player.name} earned {payouts[0]} for predicting {prediction} would win!')
                    player.money += payouts.pop(0)
            else:
                print(f'{player.name} lost 1 for predicting {prediction} would win.')
        
        loser = self.leg_loser()
        payouts = [8,5,3,2,1]
        print(f'Racer {loser} is the loser of the Race')
        for player, prediction in self.prediction_losers:
            if prediction == loser:
                if payouts[0] == 1:
                    print(f'{player.name} earned 1 for predicting {prediction} would lose!')
                    player.money += 1
                else:
                    print(f'{player.name} earned {payouts[0]} for predicting {prediction} would lose!')
                    player.money += payouts.pop(0)
            else:
                print(f'{player.name} lost 1 for predicting {prediction} would lose.')
        

    def predict_winner(self, player, racer):
        player.predictions.remove(racer)
        self.prediction_winners.append((player,racer))
        print(f'predicted winners: {self.prediction_winners}')


    def predict_loser(self, player, racer):
        player.predictions.remove(racer)
        self.prediction_losers.append((player,racer))
        print(f'predicted losers: {self.prediction_losers}')



    def get_leg_results(self, place):
        results = []
        for spot in reversed(self.board.track):
            for racer in reversed(spot):
                results.append(racer)
        return results[place - 1]
            
            
    def leg_payout(self):
        leader = self.get_leg_results(1)
        second = self.get_leg_results(2)
        print(f'The winner of this leg is Racer {self.get_leg_results(1)}')

        # pay out winners, reset winning racer's bets to empty list
        for player in self.players:
            print(f'{player.name} ended the leg with {player.money}')
            print(f'{player.name} bet on: {player.bets}')
            # payout bet amounts for any bets on the winner
            payout = 0
            if leader in player.bets:
                for bet in player.bets[leader]:
                    payout += bet
                    print(f'{player.name} earned {payout} betting on {leader}')
                player.money += payout
                del player.bets[leader]
            # payout 1 for any bets on the second place racer
            if second in player.bets:
                for bet in player.bets[second]:
                    payout += 1
                    print(f'{player.name} earned 1 betting on {second}')
                player.money += payout
                del player.bets[second]
            # after winning bets have been cleared out, calculate penalties by counting remaining bets in dict
            penalty = 0
            for bets in player.bets.values():
                for bet in bets:
                    if bet > 0:
                        penalty += 1
                
            print(f'{player.name} was penalized {penalty}')
            player.money -= penalty
            if self.phase == 'payout':
                self.phase == 'leg'

            
    def place_bet(self, player, racer):
        bet = self.bets[racer][0]
        if racer not in player.bets:
            player.bets[racer] = []
        player.bets[racer].append(bet)
        self.bets[racer].pop(0)

        print(f'Your bets: {player.bets}')


    def reset_bets(self):
        self.bets = {'A': [5,3,1], 'B': [5,3,1], 'C': [5,3,1], 'D': [5,3,1], 'E': [5,3,1]}
        for player in self.players:
            player.bets = {}


    def next_player(self):
        if self.current_player >= len(self.players)-1:
            self.current_player = 0
        else:
            self.current_player += 1

    
    def shuffle_racers(self):
        racers = ['A','B','C','D','E']
        random.shuffle(racers)
        self.board.racers = racers
        

    def spot_is_tile(self, spot):
        if len(self.board.track[spot]) > 0 and type(self.board.track[spot][0]) is tuple:
            return True
        else:
            return False
        
    def stack_unit(self, unit, spot, direction = 1):
        print('stack unit was called')
        if direction < 0:
            for r in reversed(unit):
                self.board.track[spot].insert(0, r)
        else:
            for r in unit:
                    self.board.track[spot].append(r)

        

    def roll(self):
        racer = self.board.racers[0]
        self.board.racers.pop(0)
        self.board.racers_remaining.remove(racer)
        roll = random.randint(1,3)

        # find the spot containing racer
        for i, spot in enumerate(self.board.track):
            if racer in spot:
                unit = self.get_unit(racer)
                target_spot = i + roll
                # if this roll will cross the finish line, put them at the last spot and change phase to endgame
                if target_spot >= len(self.board.track) - 1:
                    target_spot = len(self.board.track) - 1               
                    self.phase = 'endgame'
                    self.stack_unit(unit=unit, spot=target_spot)
                    self.board.racers = []
                    return
                
                if self.spot_is_tile(target_spot):
                    # grab tile info from tuple in track
                    player = self.board.track[target_spot][0][0]
                    tile_direction = self.board.track[target_spot][0][1]
                    print(f'THE CAMEL UNIT LANDED ON A TILE BELONGING TO {player}')
                    target_spot += tile_direction
                    self.stack_unit(unit=unit, spot=target_spot, direction=tile_direction)
                else:
                    print('calling stack_unit')
                    self.stack_unit(unit=unit, spot=target_spot)
                        

        self.players[self.current_player].money += 1
        print(f'### RACER: {racer}, UNIT: {unit}, ROLL: {roll} ###')

        if len(self.board.racers) == 0:
            self.phase = 'payout'
            self.shuffle_racers()
            self.board.racers_remaining = sorted(self.board.racers)   


    def get_unit(self, racer):
        unit = []
        for i, spot in enumerate(self.board.track):
            if racer in spot:
                index = spot.index(racer)
                for camel in spot[index:]:
                    unit.append(camel)
                    spot.remove(camel)
        return unit


class Board:
    
    def __init__(self) -> None:
        self.track = [[],[],[],[],[],[('player1',1)],[],[],[],[]]
        self.racers = ['A','B','C','D','E']
        random.shuffle(self.racers)
        for racer in self.racers:
            spot = random.randint(0,2)
            self.track[spot].append(racer)
        random.shuffle(self.racers)
        #set new attribute racers_remaining equal to self.racers sorted alphabetically
        self.racers_remaining = sorted(self.racers)
        #self.racers = ['🐰','🦊','🐻','🐸','🐯']

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.bets = {}
        self.predictions = ['A','B','C','D','E']
        self.money = 0
        self.has_tile = True