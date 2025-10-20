# ETL Pipeline for Weather and Flights Information of Selected Cities
The pipeline will extract data from 3 different sources, one will be web scrapping, and the other two will be using APIs. Then this data will be transformed using the Pandas library in Python. And finally, all of this clean and structured data will be stored in a SQL database.

## Data Collection: Web Scraping
Using `web scraping`, basic details such as geographical location and population of the cities is extracted. We extract these information from [Wikipedia](https://www.wikipedia.org/).

## Data Collection: APIs
We use two APIs to extract data related to the weather and flight arrivals in the selected cities. You need to obtain your own API keys to access these APIs. Place those keys in the `.env` file in the repository to load them when running the `main.ipynb` file. Make sure to name the files to suit the loading method used in the notebook and python files.

1. [OpenWeather API](https://openweathermap.org/api) is used to get weather information such as temperature, wind speed, rain in the last 3 hours, and forecast.
2. [AeroDataBox API](https://rapidapi.com/aedbx-aedbx/api/aerodatabox) is used to get the arrival information of flights in the selected cities.


## SQL Database
The `sql_commands.txt` file in the repository contains the SQL commands that we execute on MySQL workbench to create the required database with necessary tables. 

### Schema of the Database
![Schema](/images/sql_database_schema.png)

## Tools and Technologies
- Python (Pandas, Requests, BeautifulSoup)
- Jupyter Notebook