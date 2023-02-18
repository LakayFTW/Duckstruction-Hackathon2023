import random
from moebel import Moebel
import pprint
from time import sleep

FIELD_SIZE = 10
field = [['']*10]*10

init_data = None
def handle_init(data):
    global init_data
    init_data = data

last_round_result = None
def handle_result(data):
    global last_round_result
    last_round_result = data
    print('Player 1 ENDSCORE: ' + str(last_round_result['players'][0]['score']) + ' ID: ' + str(data['players'][0]['id']) + ' WIR!' if last_round_result['self'] == data['players'][0]['id'] else '')
    print('Player 2 ENDSCORE: ' + str(last_round_result['players'][1]['score']) + ' ID: ' + str(data['players'][1]['id']) + ' WIR!' if last_round_result['self'] == data['players'][1]['id'] else '')

round = 0
def handle_round(data):
    # sleep(4)
    global round
    round += 1
    print('Player 1: ' + str(data['players'][0]['score']) + ' ID: ' + str(data['players'][0]['id']))
    print('Player 2: ' + str(data['players'][1]['score']) + ' ID: ' + str(data['players'][1]['id']))
    print('Round: ' + str(round))
    print('------------------')
    pprint.pp(data['boards'][0])
    print('------------------')
    pprint.pp(data['boards'][1])
    return [random.randint(0, 9), random.randint(0, 9)]


def handle_set(data):
    global moebels
    moebels = []
    global coordlist
    coordlist = []
    while len(moebels) < len(Moebel.moebel_sizes):
        for size in Moebel.moebel_sizes:
            while True:
                x = random.randint(0, FIELD_SIZE - 1)
                y = random.randint(0, FIELD_SIZE - 1)

                direction = random.choice(['h', 'v'])

                next_moebel = Moebel(size, x, y, direction)
                # sollte checken ob moebel out of bounds gehen können
                if moebel_placable(next_moebel, size):
                    moebels.append(next_moebel)
                    break
                else:
                    continue
            
    list_of_moebel_dicts = []
    for next_moebel in moebels:
        list_of_moebel_dicts.append({
            'start': [next_moebel.x, next_moebel.y],
            'direction': next_moebel.direction,
            'size': next_moebel.size
        })
    print(list_of_moebel_dicts)
    return list_of_moebel_dicts

# def can_place_moebel(x, y, size, direction):
#     if moebels:
#         if direction == 'h':
#             if y + size > FIELD_SIZE:
#                 print(str(y + size))
#                 return False
#             for i in range(size):
#                 if [moebel for moebel in moebels if moebel.x == x and moebel.y == y+i]:
#                     return False
#         elif direction == 'v':
#             if x + size > FIELD_SIZE:
#                 print(str(x + size))
#                 return False
#             for i in range(size):
#                 if [moebel for moebel in moebels if moebel.x == x+i and moebel.y == y]:
#                     return False
#         return True
#     return True

def moebel_placable(next_moebel, size):
    placable = False
    sidestep = False
    global coordlist
    if next_moebel.x + size > FIELD_SIZE or next_moebel.y + size > FIELD_SIZE or \
        next_moebel.x < 0 or next_moebel.y < 0:
        return False

    inner = []
    for i in range(next_moebel.size):
        if next_moebel.direction == 'h':
            inner.append([next_moebel.x, next_moebel.y+i])
        else:
            inner.append([next_moebel.x+i, next_moebel.y])
    coordlist.append(inner)
    
    if moebels:
        for moebel in moebels:
            for i in range(len(coordlist)):
                for j in range(len(coordlist)):
                    if coordlist[i][j+1] != coordlist[i+1][j]:
                        test1 = coordlist[i][j+1]
                        test2 = coordlist[i+1][j]
                        if(i+1 == moebel.size and sidestep == False):
                            print("placed!")
                            placable = True
                            coordlist.append(inner)
                        else:
                            placable = False
                            inner = []
                    else:
                        print("cant place")
                        placable = False
                        sidestep = True
                        inner = []
    else:
        print("placable")
        return True
    if placable:
        placable = False
        return True
    else:
        return False

async def handle_auth(success):
    if success:
        print("Anmeldung erfolgreich")
    else:
        raise Exception('Gib mal echtes Secret')

handlers = {
    'AUTH' : handle_auth, 
    'ROUND' : handle_round, 
    'RESULT' : handle_result, 
    'SET' : handle_set, 
    'INIT' : handle_init
}