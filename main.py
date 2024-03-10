import json
import logging

from quart import Quart, websocket, make_response

from temperature import TemperatureSensor
from humidity import HumiditySensor
from light import LightSensor
from plant import Plant


clients = set()
app = Quart(__name__)

LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


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

                data_dict = json.loads(data)

                logger.info(data)

                for client in clients:
                    await client.send(data)

                    plant = Plant(
                        int(data_dict["plant_id"]),
                        data_dict["plant_name"],
                        int(data_dict["device_id"]),
                    )
                    await plant.write_on_table()
                    del plant

            # await plant.write_on_table()
            # await websocket.send("Received: " + data)
    finally:
        clients.remove(cur_obj)


@app.route("/plants/<int:id>")
async def consult_plants(id):
    plant = Plant(id)
    await plant.get_plant_info()

    data = {
        "plant_id": plant.id,
        "plant_name": plant.name,
        "plant_device_id": plant.device_id,
    }

    response = await make_response(json.dumps(data))
    return response


# Rotas necessárias:

# CRUD completo das tabelas de sensores
# consultar/escrever na tabela de planta
# consultar/escrever na tabela de sensor de umidade
# consultar/escrever na tabela de sensor de temperatura
# consultar/escrever na tab ela de sensor de luz


if __name__ == "__main__":
    app.run()
