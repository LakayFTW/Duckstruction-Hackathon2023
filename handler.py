import random
from moebel import Moebel
import pprint
from round import print_round
from copy import deepcopy
import os
import time
import generator

clear = lambda: os.system('cls') 

init_data = None
def handle_init(data):
    global init_data
    init_data = data
wins = 0
loses = 0
enemie_ships = []

class Hunt():
    def __init__(self):
        self.hunt = None
        self.hunt_start = None
        self.hunt_direction = 1
        self.hunt_orientation = Moebel.directions[0]
        self.last_choice = None
        self.hunt_direction_changed = False
        self.hunt_orientation_changed = False
        self.hunt_hits = 0
        self.hunt_possibilities = [5, 4, 3, 3, 2]

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

def get_enemy_player(data):
    players = data['players']
    return [player for player in players if player['id'] != data['self']][0]

def get_enemy_player_index(data):
    players = data['players']
    return players.index(get_enemy_player(data))

def get_enemy_map(data):
    return data['boards'][get_enemy_player_index(data)]

game_dict = {}
def handle_round(data):
    enemy_player = get_enemy_player(data)
    
    if not enemy_player['id'] in game_dict.keys():
        game_dict[enemy_player['id']] = Hunt()
        
    current_hunt = game_dict[enemy_player['id']]
    
    print(f"Gegner: {data['players'][get_enemy_player_index(data)]} ist gejagt: {current_hunt.hunt}")
    
    current_map = get_enemy_map(data)
    pprint.pp(current_map)
    
    if current_hunt.last_choice:
        print(f'Last choice: {current_hunt.last_choice}')
        print(f'Da kommen wir her: never forgetti {current_hunt.hunt_start}')
        if current_hunt.last_choice[1] > 9:
            current_hunt.last_choice = current_hunt.hunt_start
            if not current_hunt.hunt_direction_changed:
                current_hunt.hunt_direction = current_hunt.hunt_direction * -1
                current_hunt.hunt_direction_changed = True
                current_hunt.hunt_orientation_changed = False
            else:
                current_hunt.hunt_orientation = 'h' if current_hunt.hunt_orientation == 'v' else 'v'
                current_hunt.hunt_orientation_changed = True
                current_hunt.hunt_direction_changed = False
        if current_hunt.last_choice[1] < 0:
            current_hunt.last_choice = current_hunt.hunt_start
            if not current_hunt.hunt_direction_changed:
                current_hunt.hunt_direction = current_hunt.hunt_direction * -1
                current_hunt.hunt_direction_changed = True
                current_hunt.hunt_orientation_changed = False
            else:
                current_hunt.hunt_orientation = 'h' if current_hunt.hunt_orientation == 'v' else 'v'
                current_hunt.hunt_orientation_changed = True
                current_hunt.hunt_direction_changed = False
                
        if not current_hunt.hunt and current_map[current_hunt.last_choice[0]][current_hunt.last_choice[1]] == 'x':
            current_hunt.hunt = True
            current_hunt.hunt_start = current_hunt.last_choice  
        elif current_hunt.hunt and current_map[current_hunt.last_choice[0]][current_hunt.last_choice[1]] == 'X':
            current_hunt.hunt = False
            
            ship_to_remove = current_hunt.hunt_hits + 1
            if ship_to_remove in current_hunt.hunt_possibilities:
                current_hunt.hunt_possibilities.remove(current_hunt.hunt_hits + 1)
            else:
                print('HALT CARSTEN, WIR HABEN EINEN NOTFALL ' + str(current_hunt.hunt_hits))
                current_hunt.hunt_hits - 1
                current_hunt.hunt_possibilities.remove(current_hunt.hunt_hits + 1)
                
            current_hunt.hunt_hits = 0
            current_hunt.hunt_start = None
        
    if current_hunt.hunt:
        invalid_choices = 0
        
        if current_map[current_hunt.last_choice[0]][current_hunt.last_choice[1]] == 'x':
            current_hunt.hunt_hits += 1
        
        if current_map[current_hunt.last_choice[0]][current_hunt.last_choice[1]] == '.':
            current_hunt.last_choice = current_hunt.hunt_start
            
            if not current_hunt.hunt_direction_changed:
                current_hunt.hunt_direction = current_hunt.hunt_direction * -1
                current_hunt.hunt_direction_changed = True
                current_hunt.hunt_orientation_changed = False
            else:
                current_hunt.hunt_orientation = 'h' if current_hunt.hunt_orientation == 'v' else 'v'
                current_hunt.hunt_orientation_changed = True
                current_hunt.hunt_direction_changed = False
            # return handle_round(data)
         
        if current_hunt.hunt_orientation == 'v':
            if not (0 <= (current_hunt.last_choice[1] + current_hunt.hunt_direction) <= 9) or current_map[current_hunt.last_choice[0]][current_hunt.last_choice[1] + current_hunt.hunt_direction] in ['X', '.']:
                current_hunt.hunt_direction = current_hunt.hunt_direction * -1
                invalid_choices += 1
            if not (0 <= (current_hunt.last_choice[1] + current_hunt.hunt_direction) <= 9) or current_map[current_hunt.last_choice[0]][current_hunt.last_choice[1] + current_hunt.hunt_direction] in ['X', '.']:    
                current_hunt.hunt_orientation = 'h'
                invalid_choices += 1
                 
        if current_hunt.hunt_orientation == 'h':
            if not (0 <= (current_hunt.last_choice[0] + current_hunt.hunt_direction) <= 9) or current_map[current_hunt.last_choice[0] + current_hunt.hunt_direction][current_hunt.last_choice[1]] in ['X', '.']:
                current_hunt.hunt_direction = current_hunt.hunt_direction * -1
                invalid_choices += 1
            if not (0 <= (current_hunt.last_choice[0] + current_hunt.hunt_direction) <= 9) or current_map[current_hunt.last_choice[0] + current_hunt.hunt_direction][current_hunt.last_choice[1]] in ['X', '.']:    
                current_hunt.hunt_orientation = 'v'
                invalid_choices += 1
                    
        # if invalid_choices == 4:
        #     last_choice = hunt_start
        #     return handle_round(data)
            
        if current_hunt.hunt_orientation == 'v':
            choice = [current_hunt.last_choice[0], current_hunt.last_choice[1] + current_hunt.hunt_direction]
            current_hunt.last_choice = choice
            return choice
        elif current_hunt.hunt_orientation == 'h':
            choice = [current_hunt.last_choice[0] + current_hunt.hunt_direction, current_hunt.last_choice[1]]
            current_hunt.last_choice = choice
            return choice
    else:
        probabilities = [[0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0]]
        generated_maps = []
        
        start = time.time()
        while time.time() - start < 1 :
            generated_maps.append(generate_map(current_hunt.hunt_possibilities, deepcopy(current_map)))
        print(f'Woweeee {len(generated_maps)} karten generiert')
        
        for generated_map in generated_maps:
            for i in range(len(generated_map)):
                for j in range(len(generated_map[i])):
                    if generated_map[i][j] == 'O':                        
                        probabilities[i][j] += 1

        max_value = 0
        choice = None
        for i in range(len(probabilities)):
                for j in range(len(probabilities[i])):
                    value = probabilities[i][j]
                    if max_value < value:
                        max_value = value
                        choice = [i, j]
        
        current_hunt.last_choice = choice
        return choice 
    
def generate_map(ships_left, enemy_map):
    global enemie_ships
    enemie_ships = [5, 4, 3, 3, 2]
    baddies = ['x', 'X', '.', 'O']
    tries = 10
       
    for ship in ships_left:
        choice_possible = False
        choice = None
        orientation = random.choice(Moebel.directions)  
        i = 0
        while not choice_possible and i < tries:
            i += 1
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
    global last_choice, hunt, hunt_possibilities
    hunt_possibilities = [5,4,3,3,2]
    last_choice = None
    hunt = False    
    clear()
    return generator.Generator()

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
    for i in range(100):
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