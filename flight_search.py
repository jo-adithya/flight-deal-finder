from flight_data import FlightData
from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.environ.get('TEQUILA_API_KEY')
TEQUILA_ENDPOINT = 'https://tequila-api.kiwi.com'
headers = {'apikey': API_KEY}


def get_code(city):
    parameters = {
        'term': city,
        'location_types': 'city',
        'limit': 1,
    }
    response = requests.get(url=f'{TEQUILA_ENDPOINT}/locations/query', params=parameters, headers=headers)
    code = response.json()['locations'][0]['code']
    return code


def check_flights(from_city, to_city, from_date, to_date):
    parameters = {
        'fly_from': from_city,
        'fly_to': to_city,
        'date_from': from_date,
        'date_to': to_date,
        'nights_in_dst_from': 5,
        'nights_in_dst_to': 14,
        'flight_type': round,
        'one_for_city': 1,
        "max_stopovers": 2,
        'curr': 'IDR'
    }
    response = requests.get(url=f'{TEQUILA_ENDPOINT}/v2/search', params=parameters, headers=headers)

    try:
        data = response.json()["data"][0]
    except IndexError:
        print(f'No flights found for {to_city} in a span of six months.')
        return

    return FlightData(
        price=data['price'],
        airline=data['route']['airline'],
        from_city=data['route']['cityFrom'],
        to_city=data['route']['cityTo'],
        from_airport=data['route']['flyFrom'],
        to_airport=data['route']['flyTo'],
        from_date=data['route']['utc_departure'].split('T')[0] + ' UTC',
        return_date=data["route"][1]["local_departure"].split("T")[0] + ' UTC'
    )
