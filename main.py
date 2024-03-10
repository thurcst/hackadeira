from quart import Quart, websocket, make_response

from plant import Plant

app = Quart(__name__)

clients = set()


@app.route("/")
async def hello():
    return "Hello, world!"


@app.websocket("/ws")
async def devices_websocket():
    ws = await websocket.accept()
    cur_obj = websocket._get_current_object()
    clients.add(cur_obj)
    try:

        while True:
            data = await websocket.receive()
            if data == "close":
                await websocket.send("Closing the connection.")
                await websocket.close()
                break
            else:
                print(data)
                for client in clients:
                    await client.send(data)
                await websocket.send("Received: " + data)
    finally:
        clients.remove(cur_obj)


@app.route("/plants/<int:id>")
async def consult_plants(id):
    plant = Plant(id)
    response = make_response(await plant.get_info())
    return response


# Rotas necessárias:

# CRUD completo das tabelas de sensores
# consultar/escrever na tabela de planta
# consultar/escrever na tabela de sensor de umidade
# consultar/escrever na tabela de sensor de temperatura
# consultar/escrever na tab ela de sensor de luz


if __name__ == "__main__":
    app.run()
