import duckdb

cursor = duckdb.connect()
cursor.execute("select * from TABLES").fetchall()
