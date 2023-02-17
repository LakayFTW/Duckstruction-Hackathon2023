import asyncio
import socketio

SECRET = 'f6d5633c-c40e-4f73-990c-48c01f7032d7'
URL = 'https://games.uhno.de'

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('Verbunden!')
    await sio.emit('authenticate', SECRET)

async def main():
    await sio.connect(URL, transports=['websocket'])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main());