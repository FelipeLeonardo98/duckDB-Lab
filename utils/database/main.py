import duckdb
from utils.logs.main import Logger

Logger = Logger(__name__)

class DuckDBConnection():
    def __init__(self, path):
        self.path = path
        self.connection =  duckdb.connect("database_data.duckdb")
        #return connection

    def createDimCountry(self, countries_list):
        try:
            self.connection.execute('CREATE TABLE IF NOT EXISTS dim_country (id VARCHAR, name VARCHAR, iso3_code VARCHAR, year VARCHAR)')
            # connection.executemany('INSERT INTO dim_country VALUES (?,?,?,?)', countries_list) 
            """
                it was executed once, for uncomment insert lines, we can change the `CREATE TABLE` statement for `CREATE OR REPLACE`
                or, implement a logic to check date or MAX (id)
            """
            Logger.emit("Closing connection")
            self.connection.close()
        except Exception as e:
            self.connection.close()
            raise ValueError(f"Something happend wrong on `dim_country()` process. Please, try to understand the follow error: {e} . And check the logs information")
        
    def createFactGDP(self, gdp_list):
        Logger.emit("Creating `fact_gdp` table")
        try:
            self.connection.execute('CREATE TABLE IF NOT EXISTS fact_gdp (country_id VARCHAR, year VARCHAR, value FLOAT);')
            # connection.executemany('INSERT INTO fact_gdp (country_id, year, value) VALUES (?,?,?)', gdp_list)
            Logger.emit("Process finished")
            Logger.emit("Closing connection")
            self.connection.close()
        except Exception as e:
            self.connection.close()
            raise ValueError(f"Something happend wrong on `createFactGDP()` process. Please, try to understand the follow error: {e} . And check the logs information")
            
        
    def processPivotTable(self):
        Logger.emit("Starting Pivot query process")
        Logger.emit("Taking the last 5 years")
        
        lastFiveYears = self.connection.query("SELECT DISTINCT year FROM fact_gdp ORDER BY year DESC LIMIT 5").fetchall()
        lastFiveYearsList = [str(year[0]) for year in sorted(lastFiveYears)]
        Logger.emit(f"Here's the last five years {lastFiveYearsList}")

        Logger.emit("Creating the schema `refined` to store report business table. Please, check if the schema already exists, on `processPivotTable` method", category="WARNING")
        try:
            self.connection.execute("CREATE SCHEMA IF NOT EXISTS refined;")
        except Exception as e:
            self.connection.close()
            raise ValueError(f"Error when trying to create refined.business_report, check information: {e}")
        
        # Build a dynamic list for interact over the years
        selectYears = ", ".join([f"MAX(CASE WHEN g.year = '{year}' THEN value / 1e9 ELSE NULL END) AS year_{year}" for year in lastFiveYearsList]) # division by 1e9 for billion format

        # Consulta SQL de PIVOT
        pivot_query = f"""
        CREATE OR REPLACE TABLE refined.business_report AS
            SELECT
                c.id,
                c.name,
                c.iso3_code,
                {selectYears}
            FROM
                dim_country AS c
            LEFT JOIN
                fact_gdp AS g
            ON
                c.id = g.country_id
            GROUP BY
                c.id, c.name, c.iso3_code
            ORDER BY
                c.id;
        """
        try:
            create_report_table = self.connection.execute(pivot_query)
            Logger.emit("Table refined.business_report created with success!")
            report = self.connection.query("SELECT * FROM refined.business_report;").show()

            Logger.emit("Closing connection")
            
        except Exception as e:
            self.connection.close()
            raise ValueError(f"Error when trying to create refined.business_report, check information: {e}")
        
        

        
        return report
        
    