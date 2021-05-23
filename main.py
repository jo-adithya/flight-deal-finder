from flight_search import get_code, check_flights
from data_manager import DataManager
from twilio.rest import Client
from dotenv import load_dotenv
import datetime as dt
import os

load_dotenv()
ORIGIN_CITY = 'CGK'
data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()

if sheet_data[0]['iataCode'] == '':
    for city in sheet_data:
        city['iataCode'] = get_code(city['city'])
    data_manager.sheet_data = sheet_data
    data_manager.update_code()

today = dt.datetime.now()
tomorrow = (today + dt.timedelta(days=1)).strftime('%d/%m/%Y')
six_months = (today + dt.timedelta(days=6 * 30)).strftime('%d/%m/%Y')

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

for destination in sheet_data:
    flight_data = check_flights(
        from_city=ORIGIN_CITY,
        to_city=destination['iataCode'],
        from_date=tomorrow,
        to_date=six_months
    )

    if flight_data is not None and (flight_data.price < destination['lowestPrice'] or destination['lowestPrice'] == 0):
        message = client.messages.create(
            body=f"Low Price Alert!\n"
                 f"Only Rp {flight_data.price} to fly from {flight_data.from_city}-{flight_data.from_airport} "
                 f"to {flight_data.to_city}-{flight_data.to_airport}, "
                 f"from {flight_data.from_date} to {flight_data.return_date}.",
            from_=os.environ.get('VIRTUAL_PHONE'),
            to=os.environ.get('PHONE_NUMBER')
        )
        destination['lowestPrice'] = flight_data.price
data_manager.update_price()
