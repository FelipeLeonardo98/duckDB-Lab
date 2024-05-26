from utils.logs.main import Logger

Logger = Logger(__name__)
class DuckDBQueries():
    def __init__(self, connection):
        self.connection = connection
        

    def createDimCountry(self, dw, countries_list):
        # create Duck tables
        Logger.emit("Creating `dim_country` table")
        try:
            dw.execute('CREATE TABLE IF NOT EXISTS dim_country (id VARCHAR, name VARCHAR, iso3_code VARCHAR, year VARCHAR)')
            dw.executemany('INSERT INTO dim_country VALUES (?,?,?,?)', countries_list)
            Logger.emit("Process finished")
        except Exception as e:
            raise ValueError(f"Something happend wrong on `createDimCountry()` process. Please, try to understand the follow error: {e} . And check the logs information")

    def createFactGDP(self,gdp_list):
        Logger.emit("Creating `fact_gdp` table")
        try:
            self.connection.execute('CREATE TABLE IF NOT EXISTS fact_gdp (country_id VARCHAR, year VARCHAR, value FLOAT);')
            self.connection.executemany('INSERT INTO fact_gdp (country_id, year, value) VALUES (?,?,?)', gdp_list)
            Logger.emit("Process finished")
        except Exception as e:
            raise ValueError(f"Something happend wrong on `createFactGDP()` process. Please, try to understand the follow error: {e} . And check the logs information")
