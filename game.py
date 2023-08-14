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
                    print('##############GAME OVER ' + unit[-1] + ' WINS!!######################')
                    self.phase = 'end'
                    self.board.racers = []
                for r in unit:
                    spot.remove(r)
                    self.board.track[target_spot].append(r)
                break

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


    # def shuffle_racers(self):
    #     racers = ['A','B','C','D','E']
    #     random.shuffle(racers)
    #     self.racers = racers


    # def roll(self):
    #     racer = self.racers[0]
    #     print('racer: ' + racer)
    #     unit = self.get_unit(racer)
    #     roll = random.randint(1,3)
    #     print(str(unit) + ' moved ' + str(roll) + ' spaces.')

    #     for i, spot in enumerate(self.track):
    #         if racer in spot:
    #             target_spot = i + roll
    #             if target_spot >= len(self.track) - 1:
    #                 target_spot = len(self.track) - 1
    #                 print('##############GAME OVER ' + unit[-1] + ' WINS!!######################')
    #             for r in unit:
    #                 spot.remove(r)
    #                 self.track[target_spot].append(r)
    #             break   


    # def get_unit(self, racer):
    #     unit = []
    #     for i, spot in enumerate(self.track):
    #         if racer in spot:
    #             index = spot.index(racer)
    #             for camel in spot[index:]:
    #                 unit.append(camel)
    #     print('unit:' + str(unit))
    #     return unit
    

class Player:
    def __init__(self, name) -> None:
        self.name = name