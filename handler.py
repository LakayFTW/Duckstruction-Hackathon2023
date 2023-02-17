import random
from moebel import Moebel
import pprint
from time import sleep
from generate import Generator
from shoot import Shoot,Reset

round = 0

init_data = None
def handle_init(data):
    global init_data
    init_data = data

last_round_result = None
def handle_result(data):
    global last_round_result,round
    last_round_result = data
    print('Player 1 ENDSCORE: ' + str(last_round_result['players'][0]['score']) + ' ID: ' + str(data['players'][0]['id']) + ' WIR!' if last_round_result['self'] == data['players'][0]['id'] else '')
    print('Player 2 ENDSCORE: ' + str(last_round_result['players'][1]['score']) + ' ID: ' + str(data['players'][1]['id']) + ' WIR!' if last_round_result['self'] == data['players'][1]['id'] else '')
    round = 0
def handle_round(data):
    global round
    round += 1
    print('Player 1: ' + str(data['players'][0]['score']) + ' ID: ' + str(data['players'][0]['id']))
    print('Player 2: ' + str(data['players'][1]['score']) + ' ID: ' + str(data['players'][1]['id']))
    print('Round: ' + str(round))
    #print('------------------')
    #pprint.pp(data['boards'][0])
    #print('------------------')
    #pprint.pp(data['boards'][1])
    return Shoot(data)

def handle_set(data):
    Reset()
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