import duckdb
from device import Device


class Plant:
    def __init__(self, id: int, name: str = None, device_id: int = None) -> None:
        self.id = id
        self.name = name
        self.device_id = device_id

        self.conn = duckdb.connect("plants")
        self.conn.execute(
            """
             CREATE TABLE IF NOT EXISTS plants (
              plant_id INTEGER   PRIMARY KEY,
              device_id integer,
              name string
          )
          """
        )

    async def write_on_table(self):
        query = f"""
                INSERT INTO plants VALUES ({self.id}, {self.device_id}, '{self.name}') ON CONFLICT DO UPDATE SET name = EXCLUDED.name;
                """

        self.conn.execute(query=query)

    async def get_device_id(self):
        return self.device.id

    async def get_plant_info(self):
        query_results = self.conn.execute(
            f"""
        SELECT name, device_id FROM plants WHERE plant_id = {self.id}
            """
        ).fetchall()

        self.name = query_results[0][0]
        self.device_id = query_results[0][1]
        print(query_results[0])
