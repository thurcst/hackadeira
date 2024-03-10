import duckdb
from datetime import datetime


class LightSensor:
    def __init__(self, id) -> None:
        self.id = id
        self.light_values = list()
        self.conn = duckdb.connect("light-sensor")
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS light_sensor (
            light_sensor_id INTEGER PRIMARY KEY,
            time TIMESTAMP,
            light_value BOOL,
            device_id INTEGER
            );
          """
        )

    def __check_table(self):
        if len(self.light_values) == 0:
            return False
        return True

    def __compare_last_value(self):
        if self.__check_table() == False:
            return False
        if self.actual_light != self.light_values[-1]["light_value"]:
            return False
        return True

    async def write_humidity_table(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        query = f"""
                INSERT INTO light_sensor VALUES ({self.id},'{now}',{self.actual_light})
                """

        if self.__compare_last_value():
            return

        self.light_values.append(self.actual_light)
        self.conn.execute(query=query)

    async def update_actual_light(self, light):
        if self.light_values[-1] == light:
            return

        self.actual_light = light
        await self.write_light_table()

    async def read_light_table(self):
        query = f"""SELECT * FROM light_sensor WHERE light_sensor_id = {self.id}"""
        values = self.conn.execute(query=query).fetchall()
        self.light_values = values

    async def set_light(self, light: float):
        self.actual_light = light
        await self.write_light_table()

    def get_actual_light(self):
        return self.actual_light
