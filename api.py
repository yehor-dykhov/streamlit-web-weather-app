import os
from requests import get, HTTPError

# openweathermap API_KEY has to be there
API_KEY = os.environ['WEATHER_API_KEY']


def get_apip_url(city):
    return f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'


def get_weather_data(city):
    data = None

    try:
        data = get(get_apip_url(city)).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')

    if data['cod'] != '200' or data is None:
        return []

    return data['list']
