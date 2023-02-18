import asyncio
import socketio
from const import SECRET, URL
from handler import handlers
import sys

sys.setrecursionlimit(10000)

sio = socketio.AsyncClient()

@sio.event
async def connect():
    await sio.emit('authenticate', SECRET)    

@sio.event
async def data(data):
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