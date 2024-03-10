import duckdb
from datetime import datetime
import asyncio


class HumiditySensor:
    def __init__(self, id) -> None:
        self.id = id
        self.humidity_values = [False]
        self.conn = duckdb.connect("humidity-sensor")
        self.conn.execute(
            # CREATE TABLE IF NOT EXISTS humidity_sensor (
            """
             CREATE OR REPLACE TABLE humidity_sensor (
              humidity_sensor_id INTEGER PRIMARY KEY,
              time TIMESTAMP,
              humidity_value BOOL,
              device_id INTEGER
          );
          """
        )

    def __check_table(self):
        if len(self.humidity_values) == 0:
            return False
        return True

    def __compare_last_value(self):
        if self.__check_table() == False:
            return False
        if self.actual_humidity != self.humidity_values[-1]["humidity_value"]:
            return False
        return True

    async def write_humidity_table(self):
        now = now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        query = f"""
                INSERT INTO humidity_sensor VALUES ({self.id},'{now}',{self.actual_humidity})
                """

        if self.__compare_last_value():
            return

        self.humidity_values.append(self.actual_humidity)
        self.conn.execute(query=query)

    async def update_actual_humidity(self, humidity):
        if self.humidity_values[-1] == humidity:
            return

        self.actual_humidity = humidity
        await self.write_humidity_table()

    async def read_humidity_table(self):
        query = (
            f"""SELECT * FROM humidity_sensor WHERE humidity_sensor_id = {self.id}"""
        )
        values = self.conn.execute(query=query).fetchall()
        self.humidity_values = values

    async def set_humidity(self, humidity: float):
        self.actual_humidity = humidity
        await self.write_humidity_table()

    def get_actual_humidity(self):
        try:
            actual_humidity = self.actual_humidity
        except Exception:
            return None
        return actual_humidity
