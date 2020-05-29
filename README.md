# Where to drink
The script searches for the nearest 5 bars from your location and displays them on the map.

## Getting started
### Manual instruction
1. **Clone the repository** 
`
git clone https://github.com/5p1K3-wq/where_to_drink.git
`
2.  **Open directory**
`cd where_to_drink/`
3.  **We start the setup script**
`python3 setup.py`
4.  **Specify the values for the following variables:**
    *   `api_key_yandex` - Api key Yandex-geocoder. [How to get api key Yandex geocoder](https://devman.org/encyclopedia/api-docs/yandex-geocoder-api/)
5.  **Run the script `python3 main.py` and indicate where we are.**

![](https://dvmn.org/media/filer_public/05/db/05dbaec7-db70-4abc-bfe7-d859d8e6e0bc/bars-search.gif)

## Built With
[python-dotenv 0.13.0](https://pypi.org/project/python-dotenv/) - It allows you to load environment variables from the 
.env file in the root directory

[folium 0.11.0](https://pypi.org/project/folium/) - Data visualization on the map.

[geopy 1.22.0](https://pypi.org/project/geopy/) - Geopy makes it easy for Python developers to locate the coordinates of 
addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources.