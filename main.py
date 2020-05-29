import json
import os
import folium
from requests import get
from dotenv import load_dotenv
from pathlib import Path
from geopy import distance
from flask import Flask

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
API_KEY_YANDEX = os.getenv('api_key_yandex')


def fetch_coordinates(place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": API_KEY_YANDEX, "format": "json"}
    response = get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance_between_two_coordinates(where_from, to_where):
    return distance.distance(where_from, to_where).kilometers


def get_bar_distance(bar):
    return bar['distance']


def get_nearest_bars(bars_list, count_bar):
    bars_list_sort = sorted(bars_list, key=get_bar_distance)
    return bars_list_sort[:count_bar]


def show_bars():
    with open('map.html') as my_map:
        return my_map.read()


def show_bars_on_a_map():
    app = Flask(__name__)
    app.add_url_rule('/', 'where to drink', show_bars)
    app.run('0.0.0.0')


def save_bars_to_file(user_coordinates, bars):
    my_map = folium.Map(
        location=user_coordinates,
        zoom_start=13
    )

    folium.Marker(
        location=user_coordinates,
        icon=folium.Icon(color='red'),
        popup='Вы здесь!'
    ).add_to(my_map)

    for bar in bars:
        coordinates = (bar['latitude'], bar['longitude'])
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color='green'),
            popup=bar['title']
        ).add_to(my_map)
    my_map.save('map.html')


def get_bars(user_coordinates):
    with open("src/bars.json", "r", encoding="CP1251") as bars_file:
        bars_data = bars_file.read()

    bars_json = json.loads(bars_data)
    bars = []
    for bar in bars_json:
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


def main():
    where_i_am = input('Где вы находитесь? ')
    my_coordinates = fetch_coordinates(where_i_am)
    bars = get_bars(my_coordinates)
    show_number_bars = 5
    nearest_bars = get_nearest_bars(bars, show_number_bars)
    save_bars_to_file(my_coordinates, nearest_bars)
    show_bars_on_a_map()


if __name__ == '__main__':
    main()
