from dotenv import load_dotenv
import requests
import os

load_dotenv()
USERNAME = os.environ.get('SHEETY_USERNAME')
PROJECT_NAME = os.environ.get('SHEETY_PROJECT_NAME')
SHEET_NAME = os.environ.get('SHEETY_SHEET_NAME')
BEARER = os.environ.get('SHEETY_BEARER')

sheety_url = f'https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET_NAME}'
headers = {
    'Authorization': f'Bearer {BEARER}',
    'Content Type': 'application/json'
}


class DataManager:
    def __init__(self):
        self.sheet_data = {}

    def get_sheet_data(self):
        response = requests.get(url=sheety_url, headers=headers)
        self.sheet_data = response.json()['prices']
        return self.sheet_data

    def update_code(self):
        for city in self.sheet_data:
            new_data = {
                'price': {
                    'iataCode': 'IATA Code'
                }
            }
            response = requests.put(url=f'{sheety_url}/{city["id"]}', json=new_data)
            print(response.text)
