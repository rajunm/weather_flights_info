import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from lat_lon_parser import parse


def scrape_city_data(cities_list):
    ''' Scrape city data from Wikipedia and return as DataFrame 
    @param cities_list: List of city names as strings
    
    @return: DataFrame with columns city_name, country, latitude, longitude
    '''

    # Create empty list for storing data
    cities_data = []

    # Loop through cities
    for city in cities_list:

        # Create url
        url = f"https://en.wikipedia.org/wiki/{city}"
        header= {'User-Agent':"Chrome 134.0.0.0"}
        # Pull HTML
        response = requests.get(url, headers=header)
        city_soup = BeautifulSoup(response.content, 'html.parser')

        # Locate and extract data
        country = city_soup.find(string='Country').find_next('td').get_text()
        lat = city_soup.find('span', class_='latitude').get_text()
        long = city_soup.find('span', class_='longitude').get_text()

        # Create dictionary for 1 row of final data frame
        city_data = {
            'city_name': city,
            'country': country,
            'latitude': parse(lat),
            'longitude': parse(long)
        }
        # Add row to list
        cities_data.append(city_data)
    
    # Combine all rows into data frame
    return pd.DataFrame(cities_data)


def scrape_population_data(cities_df):
    ''' Scrape population data from Wikipedia and return as DataFrame
    @param cities_list: List of city names as strings
    
    @return: DataFrame with columns city_name, population, time_stamp
    '''

    # Create empty list for storing data
    cities_data = []

    # Loop through cities
    for _, city in cities_df.iterrows():

        # Create url
        url = f"https://en.wikipedia.org/wiki/{city['city_name']}"
        header= {'User-Agent':"Chrome 134.0.0.0"}
        # Pull HTML
        response = requests.get(url, headers=header)
        city_soup = BeautifulSoup(response.content, 'html.parser')

        # Locate and extract data
        pop = city_soup.find(string="Population").find_next('td').get_text()
        # Convert to integer after removing commas
        pop_int = int(pop.replace(',', ''))

        # Get the timestamp
        today = datetime.today().strftime("%d.%m.%Y")
        today = pd.to_datetime(today, format="%d.%m.%Y")

        # Create dictionary for 1 row of final data frame
        city_data = {
            'city_id':  city["city_id"],
            #'city_name': city,
            'population': pop_int,
            'timestamp_population': today
        }
        # Add row to list
        cities_data.append(city_data)

    # Combine all rows into data frame
    return pd.DataFrame(cities_data)

