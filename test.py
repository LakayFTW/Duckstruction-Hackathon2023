import asyncio
import socketio
from const import SECRET, URL
from handler import handlers

sio = socketio.AsyncClient()
field = [['']*10]*10
@sio.event
async def connect():
    print('Verbunden!')
    await sio.emit('authenticate', SECRET)    

@sio.event
async def data(data):
    print('Daten vom Typ:' + str(data['type']))
    t = data['type']
    if t in handlers:
        return handlers[t](data)
    else:
        raise Exception('Handel dein Zeuch')

async def main():
    await sio.connect(URL, transports=['websocket'])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())