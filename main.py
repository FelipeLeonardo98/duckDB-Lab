# internal libraries
from utils.logs.main import Logger
from utils.database.main import DuckDBConnection
# Python libraries
import json
import requests

# Globals variables
URL_BASE = "https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json"
QUANTITY_PER_PAGE = 0

# Init objects (instances)
Logger = Logger(__name__)

class ETLProcess():
    # def __init__(self):
    #     self.total_reponse = None

    def checkAPIresultsAmount():
        Logger.emit("Making request to retrieve total_results")

        try:
            response = requests.get(f'{URL_BASE}&page=1&per_page=1')
            response = response.json()
            total_results = response[0]['total']

            Logger.emit("Making request to extract all results possible")
            total_response = requests.get(f'{URL_BASE}&page=1&per_page={total_results}').json()
            results_per_page = total_response[0]['per_page']
        except Exception as e:
            raise ValueError(f"Something happend wrong on request API process. Please, try to understand the follow error: {e} . And check the logs information")

        Logger.emit(f'The total results is {total_results} and the results per page is {results_per_page}')
        if results_per_page == total_results:
            Logger.emit("The total results requested is the same of page results, you don't need interect over more pages")
        elif results_per_page < total_results:
            Logger.emit(f'The total results has {total_results - results_per_page} records more than results per page. Check the logs and try to increase the quantity of data per page, if you still having issues, please, develop the function `apiExtractOverPages()` to extract all data over API pages.', category="WARNING")
            Logger.emit("The script will continue running with these amount of data", category="WARNING")

        return total_response
    def apiExtractOverPages():
        """
            This method should be develop if the API changed and need to pass by a process of pagination (limited number of results in a single page).
            Probably, create a loop ("For" or "While") and stop to process and receive a response different of "http status 200" can help.
        """
        pass

    def APITransformation(data):
        Logger.emit("Separating the both biggets dictionaries")
        metadata = data[0]
        gdp_data = data[1]

        Logger.emit(f"Printing object gdp_data: {gdp_data}", category="DEBUG")
        Logger.emit(f"Printing object metadata: {metadata}", category="DEBUG")
        
        Logger.emit("Creating tuples of list with specific fields from gpd_data")

        # fact countries_value
        countries_set = {
            (record["country"]["id"], record["country"]["value"], record["countryiso3code"], record['date'])
            for record in gdp_data
        }
        # Countries dimension
        countries = [
            {"id": country[0], "name": country[1], "iso3_code": country[2], "year": country[3]}
            for country in countries_set
        ]
        # transforming countries for better management
        countries_list = list(countries_set)
        Logger.emit(f"Printing countries_list: {countries_list}", category="DEBUG")
        gdp_list = [
            (
                record["country"]["id"],
                record["date"],
                record["value"]
            )
            for record in gdp_data
        ]
        Logger.emit(f"Printing gdp_list: {gdp_list}", category="DEBUG")
        return countries_list, gdp_list

if __name__ == "__main__":
    data = ETLProcess.checkAPIresultsAmount()
    countries_list, gdp_list = ETLProcess.APITransformation(data)
    Logger.emit(f"here's the return `gdp_list` from ETLProcess.APITransformation: {countries_list}", category="DEBUG")
    Logger.emit(f"here's the return `countries_list` from ETLProcess.APITransformation: {gdp_list}", category="DEBUG")
    

