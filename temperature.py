import duckdb
from datetime import datetime

import asyncio


class TemperatureSensor:
    def __init__(self, id) -> None:
        self.id = id
        self.temperature_values = list()
        self.conn = duckdb.connect("temperature-sensor")
        self.conn.execute(
            """
             CREATE TABLE IF NOT EXISTS temperature_sensor (
              temperature_sensor_id INTEGER PRIMARY KEY,
              time TIMESTAMP,
              temperature_value FLOAT
          );
          """
        )

    async def write_temperature_table(self):
        now = now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        if self.actual_temperature == self.temperature_values[-1]:
            return

        self.temperature_values.append(self.actual_temperature)

        query = f"""
                INSERT INTO temperature_sensor VALUES ({self.id},'{now}',{self.actual_temperature})
                """
        print(query)

        self.conn.execute(query=query)

    async def read_temperature_table(self):
        query = f"""SELECT * FROM temperature_sensor WHERE temperature_sensor_id = {self.id}"""
        values = self.conn.execute(query=query).fetchall()
        self.temperature_values = values

    async def set_temperature(self, temperature: float):
        self.actual_temperature = temperature
        await self.write_temperature_table()

    def get_actual_temperature(self):
        return self.actual_temperature
