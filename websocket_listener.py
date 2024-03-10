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

        while True:
            # Espera por uma mensagem do servidor
            message = await websocket.recv()
            print(f"Mensagem recebida do servidor: {message}")


asyncio.run(websocket_client())
