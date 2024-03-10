import duckdb
from device import Device


class Plant:
    def __init__(self, id: int, name: str = None, device_id: int = None) -> None:
        self.id = id

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

    async def get_plant_info(self):
        query_results = self.conn.execute(
            f"""
        SELECT name, device_id FROM plants WHERE id = {self.id}
            """
        ).fetchall()

        self.name = None
        self.device_id = None
        print(query_results[0])
