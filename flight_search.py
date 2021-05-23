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


class FlightSearch:
    pass
