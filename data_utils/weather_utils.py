import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
from pytz import timezone

load_dotenv()

# Access your API key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def fetch_weather_data(cities_df):
  '''
  Fetch 5-day weather forecast data for each city in the cities_df DataFrame.
  @param cities_df: DataFrame with columns 'city_id', 'city_name', 'latitude', 'longitude'
  @return: DataFrame containing weather forecast data with corresponding 'city_id' values
  '''
  berlin_timezone = timezone('Europe/Berlin')
  weather_items = []

  for _, city in cities_df.iterrows():
      # city_geo_data = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city['city_name']},{'DE'}&appid={WEATHER_API_KEY}").json()
      
      latitude =  city["latitude"]   # city_geo_data[0]['lat']
      longitude = city["longitude"]  #
      city_id = city["city_id"]

      url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric"
      response = requests.get(url)
      weather_data = response.json()

      retrieval_time = datetime.now(berlin_timezone).strftime("%Y-%m-%d %H:%M:%S")

      for item in weather_data["list"]:
          weather_item = {
              "city_id": city_id,
              "forecast_time": item.get("dt_txt"),
              "temperature": item["main"].get("temp"),
              "forecast": item["weather"][0].get("main"),
              "rain_in_last_3h": item.get("rain", {}).get("3h", 0),
              "wind_speed": item["wind"].get("speed"),
              "data_retrieved_at": retrieval_time
          }
          weather_items.append(weather_item)

  weather_df = pd.DataFrame(weather_items)
  weather_df["forecast_time"] = pd.to_datetime(weather_df["forecast_time"])
  weather_df["data_retrieved_at"] = pd.to_datetime(weather_df["data_retrieved_at"])

  return weather_df