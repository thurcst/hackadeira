import asyncio
import websockets
import json


async def websocket_client():
    async with websockets.connect("ws://localhost:5000/ws") as websocket:
        tmp = {
            "temperature": "23.40",
            "humidity": "62.20",
            "luminosity": "208",
            "humidityGround": "364",
        }
        await websocket.send(json.dumps(tmp))
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(websocket_client())
