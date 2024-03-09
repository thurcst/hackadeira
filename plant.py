import duckdb
from device import Device


class Plant:
    def __init__(self, id: int, name: str, device_id: int) -> None:
        self.id = id
        self.name = name
        self.device = Device(device_id)
        self.conn = duckdb.connect("plants")
        self.conn.execute(
            """
             CREATE TABLE IF NOT EXISTS plants (
              plant_id INTEGER PRIMARY KEY,
              device_id integer,
              name string
          );
          """
        )
        self.write_on_table()

    async def write_on_table(self):
        query = f"""
                INSERT INTO plants VALUES ({self.id}, '{self.name}',{self.device.id}) ON CONFLICT DO UPDATE;
                """
        print(query)

        self.conn.execute(query=query)

    async def get_device_id(self):
        return self.device.id
