import duckdb
from datetime import datetime

from humidity import HumiditySensor
from temperature import TemperatureSensor


class Device:
    def __init__(self, id) -> None:
        self.id = id
        self.humidity_sensor = None
        self.temperature_sensor = None

        self.conn = duckdb.connect("devices")
        self.conn.execute(
            """
             CREATE TABLE IF NOT EXISTS devices (
              device_id INTEGER PRIMARY KEY,
              humidity_sensor_id INTEGER,
              temperature_sensor_id INTEGER,
          );
          """
        )

    async def fetch_device_sensors(self):
        query = f"SELECT * FROM devices WHERE device_id = {self.id}"
        data = self.conn.execute(query=query).fetchall()
        if len(data) > 0:
            if self.humidity_sensor == None:
                self.humidity_sensor = HumiditySensor(data[0]["humidity_sensor_id"])
            if self.temperature_sensor == None:
                self.temperature_sensor = TemperatureSensor(
                    data[0]["temperature_sensor_id"]
                )
            return 200
        else:
            return 404
