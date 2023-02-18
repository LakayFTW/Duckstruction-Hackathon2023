round = 0
def print_round(data):
    global round
    round += 1
    print('Round: ' + str(round))
    print('------------------')
    pprint.pp(data['boards'][0])
    print('------------------')
    pprint.pp(data['boards'][1])