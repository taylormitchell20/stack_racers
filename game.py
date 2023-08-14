import random

class Game:
    def __init__(self, player_names) -> None:
        self.board = Board()
        self.shuffle_racers()
        self.board.starting_positions()
        self.current_player = 0
        self.players = []
        for player in player_names:
            p = Player(player)
            self.players.append(p)
        self.phase = 'race' # might need to change to int
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
            for bet in player.bets[leader]:
                player.money += bet
                print(f'{player.name} earned {bet} betting on {leader}')
                _ = input('')
            player.bets[leader] = []
            # after winners have been cleared out, calculate penalties by counting remaining bets in dict
            penalty = 0
            for bets in player.bets.values():
                for bet in bets:
                    print(bet)
                    if bet > 0:
                        penalty += 1
                    print(f'penalty total: {penalty}')
                
            print(f'{player.name} was penalized {penalty}')
            player.money = player.money - penalty
            _ = input('')

            


    def place_bet(self, player, racer):
        bet = self.bets[racer][0]
        player.bets[racer].append(bet)
        self.bets[racer].pop(0)

        print(player.bets)

        

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
        unit = self.get_unit(racer)
        roll = random.randint(1,3)

        for i, spot in enumerate(self.board.track):
            if racer in spot:
                target_spot = i + roll
                if target_spot >= len(self.board.track) - 1:
                    target_spot = len(self.board.track) - 1
                    
                    self.phase = 'end'
                    self.board.racers = []
                for r in unit:
                    spot.remove(r)
                    self.board.track[target_spot].append(r)
                break

        self.players[self.current_player].money += 1
        print(f'### RACER: {racer}, UNIT: {unit}, ROLL: {roll} ###')   


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
        
        self.racers = []
        #self.racers = ['🐰','🦊','🐻','🐸','🐯']
        self.track = [[],[],[],[],[],[],[],[],[],[]]
        
        
    def starting_positions(self):
        racers = self.racers
        for racer in racers:
            spot = random.randint(0,2)
            self.track[spot].append(racer)

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.bets = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[]}
        self.money = 0