import asyncio
import websockets


async def websocket_client():
    async with websockets.connect("ws://localhost:5000/ws") as websocket:
        await websocket.send("Hello, server!")
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(websocket_client())
