from notification_manager import NotificationManager
from flight_search import get_code, check_flights
from data_manager import DataManager
import datetime as dt

ORIGIN_CITY = 'CGK'
data_manager = DataManager()
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheet_data()

if sheet_data[0]['iataCode'] == '':
    for city in sheet_data:
        city['iataCode'] = get_code(city['city'])
    data_manager.sheet_data = sheet_data
    data_manager.update_code()

today = dt.datetime.now()
tomorrow = (today + dt.timedelta(days=1)).strftime('%d/%m/%Y')
six_months = (today + dt.timedelta(days=6 * 30)).strftime('%d/%m/%Y')

for destination in sheet_data:
    flight_data = check_flights(
        from_city=ORIGIN_CITY,
        to_city=destination['iataCode'],
        from_date=tomorrow,
        to_date=six_months
    )

    if flight_data is None:
        destination['lowestPrice'] = 'No Flights'
        continue

    if flight_data.price < destination['lowestPrice'] or destination['lowestPrice'] == 0:
        users = data_manager.get_user_emails()
        user_details = [(row['email'], ' '.join([row['firstName'], row['lastName']])) for row in users]

        message = f'Low Price Alert!\n' \
                  f'Only Rp {flight_data.price} to fly from {flight_data.from_city}-{flight_data.from_airport} ' \
                  f'to {flight_data.to_city}-{flight_data.to_airport}, ' \
                  f'from {flight_data.from_date} to {flight_data.return_date}.'

        if flight_data.stop_over > 0:
            message += f'\nFlight has {flight_data.stop_over} stop over, via {flight_data.via_city}'

        notification_manager.send_sms(message)

        link = f'https://www.google.co.uk/flights?hl=en#flt={flight_data.from_airport}.{flight_data.to_airport}.' \
               f'{flight_data.from_date}*{flight_data.to_airport}.{flight_data.from_airport}.{flight_data.return_date}'
        notification_manager.send_emails(user_details, message, link)

        destination['lowestPrice'] = flight_data.price
data_manager.update_price()
