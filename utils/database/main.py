import duckdb

class DuckDBConnection():
    def __init__(self, path):
        self.path = path
        con = duckdb.connect(database=path)