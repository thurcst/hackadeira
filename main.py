from quart import Quart, websocket

app = Quart(__name__)


@app.route("/")
async def hello():
    print("irra")
    return "Hello, world!"


@app.websocket("/ws")
async def devices_websocket():
    ws = await websocket.accept()
    while True:
        data = await websocket.receive()
        if data == "close":
            await websocket.send("Closing the connection.")
            await websocket.close()
            break
        else:
            print(data)
            await websocket.send("Received: " + data)


# Rotas necessárias:


# CRUD completo das tabelas de sensores
# consultar/escrever na tabela de planta
# consultar/escrever na tabela de sensor de umidade
# consultar/escrever na tabela de sensor de temperatura
# consultar/escrever na tab ela de sensor de luz


if __name__ == "__main__":
    app.run()
