import random
from moebel import Moebel
import pprint
from round import print_round
from copy import deepcopy
from generate import Generator

init_data = None
def handle_init(data):
    global init_data
    init_data = data
wins = 0
loses = 0
enemie_ships = []

def handle_result(data):
    global wins, loses
    
    player = get_player(data)
    if player['score'] > 0:
        wins += 1
        print('Won!')
    else:
        print('Lost!')
        loses += 1
    print(f'Loses: {loses} Wins: {wins}')

def get_player(data):
    players = data['players']
    return [player for player in players if player['id'] == data['self']][0]

def get_enemy_player_index(data):
    players = data['players']
    result = [player for player in players if player['id'] != data['self']][0]
    return players.index(result)

def get_enemy_map(data):
    return data['boards'][get_enemy_player_index(data)]

last_choice = None
hunt_start = None
hunt_direction = 1
hunt_orientation = Moebel.directions[0]
hunt = False
def handle_round(data):
    global enemie_ships, hunt, hunt_start, hunt_direction, hunt_orientation, last_choice
    print(f"Gegner: {data['players'][get_enemy_player_index(data)]}")
    
    current_map = get_enemy_map(data)
    #pprint.pp(current_map)
    
    if last_choice:
        print(f'Last choice: {last_choice}')
        if last_choice[1] > 9:
                last_choice[1] -= 1
        if last_choice[1] < 0:
            last_choice[1] += 1
        if not hunt and current_map[last_choice[0]][last_choice[1]] == 'x':
            hunt = True
            hunt_start = last_choice  
        elif current_map[last_choice[0]][last_choice[1]] == 'X':
            hunt = False
        
    if hunt:
        invalid_choices = 0
        
        #rework 
        if hunt_orientation == 'v':
            if not (0 < (last_choice[1] + hunt_direction) < 9) or current_map[last_choice[0]][last_choice[1] + hunt_direction] in ['X', 'x', '.']:
                hunt_direction = hunt_direction * -1
                invalid_choices += 1
            if not (0 < (last_choice[1] + hunt_direction) < 9) or current_map[last_choice[0]][last_choice[1] + hunt_direction] in ['X', 'x', '.']:    
                hunt_orientation = 'h'
                invalid_choices += 1
                 
        if hunt_orientation == 'h':
            if not (0 < (last_choice[0] + hunt_direction) < 9) or current_map[last_choice[0] + hunt_direction][last_choice[1]] in ['X', 'x', '.']:
                hunt_direction = hunt_direction * -1
                invalid_choices += 1
            if not (0 < (last_choice[0] + hunt_direction) < 9) or current_map[last_choice[0] + hunt_direction][last_choice[1]] in ['X', 'x', '.']:    
                hunt_orientation = 'v'
                invalid_choices += 1
                    
        if invalid_choices == 4:
            last_choice = hunt_start
            return handle_round(data)
            
        if hunt_orientation == 'v':
            choice = [last_choice[0], last_choice[1] + hunt_direction]
            last_choice = choice
            return choice
        elif hunt_orientation == 'h':
            choice = [last_choice[0] + hunt_direction, last_choice[1]]
            last_choice = choice
            return choice
    else:
        # print('!!!TEST!!! GENERIERTE MÖGLICHKEIT')
        # possibilites = [generate_map(enemie_ships, deepcopy(current_map)) for i in range(100)]
        # pprint.pp(possibilites)    
        # print('__________________________________')
        choice = [random.randint(0, 9), random.randint(0, 9)]
        
        while current_map[choice[0]][choice[1]] in ['X', 'x', '.']:
            choice = [random.randint(0, 9), random.randint(0, 9)]
            
        current_map[choice[0]][choice[1]] = 'x'
        
        last_choice = choice
        
        return choice

def generate_map(ships_left, enemy_map):
    global enemie_ships
    enemie_ships = [5, 4, 3, 3, 2]
    baddies = ['x', 'X', '.', 'O']
       
    for ship in ships_left:
        choice_possible = False
        choice = None
        orientation = random.choice(Moebel.directions)  
        
        while not choice_possible:
            choice = [random.randint(0, 9), random.randint(0, 9)]
            choice_possible = not enemy_map[choice[0]][choice[1]] in baddies
            if choice_possible:
                for i in range(ship):
                    if orientation == 'h':
                        if choice[0] + i > 9:
                            choice_possible = False    
                        next_choice = [choice[0] + i, choice[1]]
                    elif orientation == 'v':
                        if choice[1] + i > 9:
                            choice_possible = False
                        next_choice = [choice[0], choice[1] + i]
                    else:
                        raise Exception('Bitte Was????')
                    
                    if not choice_possible:
                        break
                    
                    upper_neighbour = [next_choice[0] + 1, next_choice[1]]
                    lower_neighbour = [next_choice[0] - 1, next_choice[1]]
                    left_neighbour = [next_choice[0], next_choice[1] - 1]
                    right_neighbour = [next_choice[0], next_choice[1] + 1]

                    choice_possible = choice_possible and not enemy_map[next_choice[0]][next_choice[1]] in baddies  
                    if not upper_neighbour[0] > 9:
                        choice_possible = choice_possible and not enemy_map[upper_neighbour[0]][upper_neighbour[1]] in ['X', 'x', 'O']
                    if not lower_neighbour[0] < 0:
                        choice_possible = choice_possible and not enemy_map[lower_neighbour[0]][lower_neighbour[1]] in ['X', 'x', 'O']
                    if not left_neighbour[1] < 0:
                        choice_possible = choice_possible and not enemy_map[left_neighbour[0]][left_neighbour[1]] in ['X', 'x', 'O']
                    if not right_neighbour[1] > 9:
                        choice_possible = choice_possible and not enemy_map[right_neighbour[0]][right_neighbour[1]] in ['X', 'x', 'O']
                    
                    if not choice_possible:
                        break
                    
        if choice_possible:
            for i in range(ship):
                if orientation == 'h':
                    enemy_map[choice[0] + i][choice[1]] = 'O'
                elif orientation == 'v':
                    enemy_map[choice[0]][choice[1] + i] = 'O'
    return enemy_map   
                    

def handle_set(data):
    global last_choice, hunt
    last_choice = None
    hunt = False    
    return Generator()

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

if __name__ == '__main__':
    for i in range(250):
        maps = [['','','','','','','','','',''],
            ['','','','','','','','','',''],
            ['','','','','','','','','',''],
            ['','','','','','','','','',''],
            ['','','X','X','X','','','','',''],
            ['','','','','','','','','',''],
            ['','','','','','','','','',''],
            ['','','','','','','','','',''],
            ['','','','','','','','','',''],
            ['','','','','','','','','','']]
        
        generated_map = generate_map([2, 2, 2, 2, 2], maps)
        pprint.pp(generated_map) 