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
        self.bets = {'A': [5,3,1], 'B': [5,3,1], 'C': [5,3,1], 'D': [5,3,1], 'E': [5,3,1]}
        
    def leg_leader(self):
        for spot in reversed(self.board.track):
            if len(spot) > 0:
                return spot[-1]
            
    def leg_payout(self):
        leader = self.leg_leader()

        # pay out winners, reset winning racer's bets to empty list
        for player in self.players:
            print(f'{player.name} ended the leg with {player.money}')
            print(f'{player.name} bet on: {player.bets}')
            payout = 0
            for bet in player.bets[leader]:
                payout += bet
                print(f'{player.name} earned {payout} betting on {leader}')
            player.money += payout
            player.bets[leader] = []
            # after winners have been cleared out, calculate penalties by counting remaining bets in dict
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
        player.bets[racer].append(bet)
        self.bets[racer].pop(0)

        print(f'Your bets: {player.bets}')

        

    def reset_bets(self):
        self.bets = {'A': [5,3,1], 'B': [5,3,1], 'C': [5,3,1], 'D': [5,3,1], 'E': [5,3,1]}
        for player in self.players:
            player.bets = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[]}


    def next_player(self):
        if self.current_player >= len(self.players)-1:
            self.current_player = 0
        else:
            self.current_player += 1

    
    def shuffle_racers(self):
        racers = ['A','B','C','D','E']
        random.shuffle(racers)
        self.board.racers = racers
        

    def roll(self):
        racer = self.board.racers[0]
        self.board.racers.pop(0)
        self.board.racers_remaining.remove(racer)
        unit = self.get_unit(racer)
        roll = random.randint(1,3)

        for i, spot in enumerate(self.board.track):
            if racer in spot:
                target_spot = i + roll
                if target_spot >= len(self.board.track) - 1:
                    target_spot = len(self.board.track) - 1
                    
                    self.phase = 'endgame'
                    self.board.racers = []
                for r in unit:
                    spot.remove(r)
                    self.board.track[target_spot].append(r)
                break

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
        return unit




class Board:
    
    def __init__(self) -> None:
        self.track = [[],[],[],[],[],[],[],[],[],[]]
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
        self.bets = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[]}
        self.money = 0