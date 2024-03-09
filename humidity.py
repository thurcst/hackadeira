import duckdb
from datetime import datetime


class HumiditySensor:
    def __init__(self, id) -> None:
        self.id = id
        self.humidity_values = list()
        self.conn = duckdb.connect("humidity-sensor")
        self.conn.execute(
            """
             CREATE TABLE IF NOT EXISTS humidity_sensor (
              humidity_sensor_id INTEGER PRIMARY KEY,
              time TIMESTAMP,
              humidity_value FLOAT
          );
          """
        )

    async def write_humidity_table(self):
        now = now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        if self.actual_humidity == self.humidity_values[-1]:
            return

        self.humidity_values.append(self.actual_humidity)

        query = f"""
                INSERT INTO humidity_sensor VALUES ({self.id},'{now}',{self.actual_humidity})
                """
        print(query)

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
        return self.actual_humidity
