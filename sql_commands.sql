-- Delete if the database already exists
DROP DATABASE IF EXISTS gans_weather ;

-- Create and use the database
CREATE DATABASE gans_weather;
USE gans_weather;


-- Create the required tables

CREATE TABLE cities (
    city_id INT AUTO_INCREMENT,
    city_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    PRIMARY KEY (city_id)
);


CREATE TABLE population (
	cities_data_id INT AUTO_INCREMENT,
    city_id INT NOT NULL,
    population INT NOT NULL,
    timestamp_population DATETIME NOT NULL,
    PRIMARY KEY (cities_data_id),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);


CREATE TABLE weather (
city_id INT NOT NULL,
temperature FLOAT,
wind_speed FLOAT,
rain_in_last_3h FLOAT,
forecast VARCHAR(255),
data_retrieved_at DATETIME NOT NULL,
forecast_time DATETIME NOT NULL,
PRIMARY KEY (city_id, forecast_time),
FOREIGN KEY (city_id) REFERENCES cities(city_id)
);



CREATE TABLE cities_airports (
    icao_code VARCHAR(10) NOT NULL,
    airport_name VARCHAR(255) NOT NULL,
    city_id INT NOT NULL,
    PRIMARY KEY (icao_code),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);


CREATE TABLE flights (
    id INT AUTO_INCREMENT,
    arrival_airport_icao VARCHAR(10),
    departure_airport_icao VARCHAR(10),
    scheduled_arrival_time DATETIME,
    flight_number VARCHAR(20),
    timestamp_flight DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (arrival_airport_icao) REFERENCES cities_airports(icao_code)
);
