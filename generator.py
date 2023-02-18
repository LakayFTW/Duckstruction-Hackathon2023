import pprint
import random
from moebel import Moebel

moebels = []
startposition = [(1,1),(4,1),(6,4),(2,7),(4,9)]
startsize = [3,4,3,2,5]
startdir = ["v","h","h","v","h"]
counter = 0
list_of_moebel_dicts = []

def Generator():    
    global counter 
    global list_of_moebel_dicts
    counter = 0  
    moebels.clear()
    for size in Moebel.moebel_sizes:
        direction = startdir[counter]
        next_moebel = Moebel(startsize[counter],
                            startposition[counter][0],
                            startposition[counter][1],
                            direction)
        moebels.append(next_moebel)
        counter += 1

    list_of_moebel_dicts.clear()
    for next_moebel in moebels:
        list_of_moebel_dicts.append({
            'start': [next_moebel.x, next_moebel.y],
            'direction': next_moebel.direction,
            'size': next_moebel.size
            })
    pprint.pp(list_of_moebel_dicts)
    return list_of_moebel_dicts