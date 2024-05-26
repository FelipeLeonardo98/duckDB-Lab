# duckDB-Lab

### Goal

The objective of this test is to develop a data ingestion pipeline using Python, which will:

* **Extract** data on the Gross Domestic Product (GDP) of South American countries using the World Bank API:
  * Endpoint: `https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json&page=1&per_page=50`

* **Load** this data into a SQL database of your choice (such as PostgreSQL, SQLite, DuckDB, Trino, etc.):
  * Create `country` (id, name, iso3_code) and `gdp` (country_id, year, value) tables.
  * Additional structures or control columns may be implemented as needed.

* **Query** the loaded data to produce a pivoted report of the last 5 years for each country, presented in Billions:
  * Expected query structure:

    | id | name     | iso3_code | 2019 | 2020 | 2021 | 2022 | 2023 |
    |----|----------|-----------|------|------|------|------|------|