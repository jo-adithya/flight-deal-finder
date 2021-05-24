from dotenv import load_dotenv
import requests
import os

load_dotenv()
USERNAME = os.environ.get('SHEETY_USERNAME')
PROJECT_NAME = os.environ.get('SHEETY_PROJECT_NAME')
SHEET_NAME = os.environ.get('SHEETY_SHEET_NAME')
BEARER = os.environ.get('SHEETY_BEARER')

sheety_url = f'https://api.sheety.co/{USERNAME}/{PROJECT_NAME}'
headers = {
    'Authorization': f'Bearer {BEARER}',
    'Content Type': 'application/json'
}


class DataManager:
    def __init__(self):
        self.sheet_data = {}
        self.users = {}

    def get_sheet_data(self):
        response = requests.get(url=f'{sheety_url}/prices', headers=headers)
        self.sheet_data = response.json()['prices']
        for data in self.sheet_data:
            price = data.get('lowestPrice')
            if price is None or price == '' or price == 'No Direct Flight':
                data['lowestPrice'] = 0
        return self.sheet_data

    def update_code(self):
        for city in self.sheet_data:
            new_data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            requests.put(url=f'{sheety_url}/prices/{city["id"]}', json=new_data, headers=headers)

    def update_price(self):
        for city in self.sheet_data:
            new_data = {
                'price': {
                    'lowestPrice': city['lowestPrice']
                }
            }
            requests.put(url=f'{sheety_url}/prices/{city["id"]}', json=new_data, headers=headers)

    def get_user_emails(self):
        response = requests.get(url=f'{sheety_url}/users', headers=headers)
        self.users = response.json()['users']
        return self.users

    @staticmethod
    def add_new_user(first_name, last_name, email, confirm_email):
        if email != confirm_email or len(first_name) == 0:
            return
        new_data = {
            'user': {
                'firstName': first_name,
                'lastName': last_name,
                'email': email
            }
        }
        response = requests.post(url=f'{sheety_url}/users', json=new_data, headers=headers)
        print(response.text)
