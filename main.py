import random
import board

b1 = board.Board()
print('#####STARTING POSITIONS########')
print(b1.track)
print('###############################')
for i in range(15):
    b1.roll()
    print(b1.track)
    print('racers left: ' + str(b1.racers))

lst = ['','','']
print(len(lst))