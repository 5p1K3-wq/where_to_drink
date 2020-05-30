import json
import folium
import os
from requests import get
from dotenv import load_dotenv, find_dotenv
from geopy import distance
from flask import Flask

load_dotenv(find_dotenv())
API_KEY = os.getenv('API_KEY')


def fetch_coordinates(place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": API_KEY, "format": "json"}
    response = get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance_between_two_coordinates(where, to):
    return distance.distance(where, to).kilometers


def get_bar_distance(bar):
    return bar['distance']


def get_nearest_bars(bars, count_bar):
    return sorted(bars, key=get_bar_distance)[:count_bar]


def show_bars():
    with open('map.html') as map:
        return map.read()


def show_bars_on_a_map():
    app = Flask(__name__)
    app.add_url_rule('/', 'where to drink', show_bars)
    app.run('0.0.0.0')


def save_bars_to_file(user_coordinates, bars):
    map = folium.Map(
        location=user_coordinates,
        zoom_start=13
    )

    folium.Marker(
        location=user_coordinates,
        icon=folium.Icon(color='red'),
        popup='Вы здесь!'
    ).add_to(map)

    for bar in bars:
        coordinates = (bar['latitude'], bar['longitude'])
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color='green'),
            popup=bar['title']
        ).add_to(map)
    map.save('map.html')


def get_bars(user_coordinates):
    with open("src/bars.json", "r", encoding="CP1251") as file:
        file_data = file.read()

    contents = json.loads(file_data)
    bars = []
    for bar in contents:
        lat = bar['geoData']['coordinates'][1]
        lon = bar['geoData']['coordinates'][0]
        bar_coordinates = (lat, lon)
        bars.append(
            {
                'distance': get_distance_between_two_coordinates(bar_coordinates, user_coordinates),
                'latitude': lat,
                'longitude': lon,
                'title': bar['Name']
            }
        )
    return bars


def def_main():
    location = input('Где вы находитесь? ')
    user_coordinates = fetch_coordinates(location)
    bars = get_bars(user_coordinates)
    show_number_bars = 5
    nearest_bars = get_nearest_bars(bars, show_number_bars)
    save_bars_to_file(user_coordinates, nearest_bars)
    show_bars_on_a_map()


if __name__ == '__main__':
    def_main()
