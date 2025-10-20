import requests
from pytz import timezone
import os
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

FLIGHT_API_key = os.getenv("FLIGHT_API_key")

def get_airports(cities_df):
  '''
  Fetch airports within 50 km radius for each city in the cities_df DataFrame.
  @param cities_df: DataFrame with columns 'city_id', 'latitude', 'longitude'
  @return: DataFrame containing airports data with corresponding 'city_id' values
  '''


  # API headers
  headers = {
      "X-RapidAPI-Key": FLIGHT_API_key,
      "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
  }

  querystring = {"withFlightInfoOnly": "true"}

  # DataFrame to store results
  all_airports = []

  for id, lat, lon in zip(cities_df['city_id'].tolist(), cities_df['latitude'].tolist(), cities_df['longitude'].tolist()):
    # Construct the URL with the latitude and longitude
    url = f"https://aerodatabox.p.rapidapi.com/airports/search/location/{lat}/{lon}/km/50/16"

    # Make the API request
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
      data = response.json()
      airports = pd.json_normalize(data.get('items', []))
      airports['city_id'] = id
      all_airports.append(airports)

  return pd.concat(all_airports, ignore_index=True)


def fetch_airports_data(airports_df):
    '''
    Fetch arrival flight data for each airport in the airports_df DataFrame.
    @param airports_df: DataFrame with column 'icao_code'
    @return: DataFrame containing arrival flight data for the airports    
    '''
    berlin_timezone = timezone('Europe/Berlin')
    airport_items = []

    for _, airport in airports_df.iterrows():
        # today = datetime.today().strftime("%Y-%m-%d")
        # query_date = (today + timedelta(days=1))
        today = datetime.now(berlin_timezone).date()
        query_date = (today + timedelta(days=1))  # Tomorrow's date
        times = [["00:00","11:59"],
             ["12:00","23:59"]]
        for time in times:
          url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{airport['icao_code']}/{query_date}T{time[0]}/{query_date}T{time[1]}"

          querystring = {"withLeg":"true","direction":"Arrival","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

          headers = {"X-RapidAPI-Key": FLIGHT_API_key,
                      "x-rapidapi-host": "aerodatabox.p.rapidapi.com"}

          response = requests.get(url, headers=headers, params=querystring)

          for item in response.json()['arrivals']:

              retrieval_time = datetime.now(berlin_timezone).strftime("%Y-%m-%d %H:%M:%S")

              airport_item = {
              "arrival_airport_icao": airport['icao_code'],
              "departure_airport_icao": item['departure']['airport'].get('icao', None),
              "scheduled_arrival_time": item['arrival']['scheduledTime'].get('local', None),    #['local'],
              "flight_number": item.get('number', None),
              "timestamp_flight": retrieval_time
              }
              airport_items.append(airport_item)

    airport_flights_df = pd.DataFrame(airport_items)
    #print(airport_flights_df)
    airport_flights_df["scheduled_arrival_time"] = pd.to_datetime(airport_flights_df["scheduled_arrival_time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    airport_flights_df["timestamp_flight"] = pd.to_datetime(airport_flights_df["timestamp_flight"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    return airport_flights_df