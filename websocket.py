import asyncio
import websockets
import json
import datetime


async def websocket_client():
    async with websockets.connect("ws://localhost:5000/ws") as websocket:
        tmp = {
            "temperature_sensor_id": "500",
            "light_sensor_id": "500",
            "humidity_sensor_id": "500",
            "device_id": "200",
            "plant_id": "10203",
            "plant_name": "dev_plant",
            "timestamp": str(datetime.datetime.now()),
            "temperature": "27.40",
            "humidity": "62.20",
            "luminosity": "208",
            "humidityGround": "1000",
        }
        await websocket.send(json.dumps(tmp))
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(websocket_client())
