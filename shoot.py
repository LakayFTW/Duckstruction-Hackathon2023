import random
import pprint

field = []
enemyboard = []
shotX = 0
shotY = 0
counter = 0
i = 0
j = 0
board = 0
fieldFree = False
previous = ""
lastshot = []

def Shoot(data = []):
    global shotX,shotY,fieldFree,field,counter,board,enemyboard,previous,i,j,lastshot
    i = 0
    j = 0
    if(data["players"][0]["id"] == data["self"]):
        board = 1
    else:
        board = 0
    enemyboard = data["boards"][board]
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(10):
        for j in range(10):
            if(enemyboard[i][j] == 'x'):
                print("Feld" + str([(i),(j)]) + "ist getroffen!!!!")
        #pprint.pp(enemyboard[i])
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(enemyboard[lastshot[0],lastshot[1]])
    print(lastshot[0,0])
    while fieldFree == False:
        for i in range(10):
            for j in range(10):
                if(enemyboard[lastshot[0,0]] == 'x'):
                    print("Letzter Schuss hat getroffen!")
        shotX = random.randint(0,9)
        shotY = random.randint(0,9)
        if (field[shotX][shotY] == 'Free'):
            fieldFree = True
            field[shotX][shotY] = "X"
            lastshot = [(shotX)][(shotY)]
    print("In Feld" + str([(shotX), (shotY)]) + "geschossen")
    fieldFree = False
    counter = 0
    return [(shotX), (shotY)]

def Reset():
    global i,j,counter
    i = 0
    j = 0
    field.clear()
    for i in range(10):
        inner = []
        for j in range(10):
            inner.append("Free")
        field.append(inner)