import random

class Board:
    
    def __init__(self) -> None:
    
        self.racers = ['A','B','C','D','E']
        #self.racers = ['🐰','🦊','🐻','🐸','🐯']
        self.track = []
        for i in range(10):
            self.track.append([])
        self.starting_spots()
        

    def starting_spots(self):
        racers = self.racers
        random.shuffle(racers)
        for racer in racers:
            spot = random.randint(0,2)
            self.track[spot].append(racer)

        

    def roll(self):
        racer = random.choice(self.racers)
        self.racers.remove(racer)
        if len(self.racers) == 0:
            self.racers = ['A','B','C','D','E']
        print('racer: ' + racer)
        unit = self.get_unit(racer)
        roll = random.randint(1,3)
        print(str(unit) + ' moved ' + str(roll) + ' spaces.')

        for i, spot in enumerate(self.track):
            if racer in spot:
                target_spot = i + roll
                if target_spot >= len(self.track) - 1:
                    target_spot = len(self.track) - 1
                    print('##############GAME OVER ' + unit[-1] + ' WINS!!######################')
                for r in unit:
                    spot.remove(r)
                    self.track[target_spot].append(r)
                break   


    def get_unit(self, racer):
        unit = []
        for i, spot in enumerate(self.track):
            if racer in spot:
                index = spot.index(racer)
                for camel in spot[index:]:
                    unit.append(camel)
        print('unit:' + str(unit))
        return unit