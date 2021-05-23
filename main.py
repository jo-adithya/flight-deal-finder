from data_manager import DataManager
from flight_search import get_code

data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()

if sheet_data[0]['iataCode'] == '':
    for city in sheet_data:
        city['iataCode'] = get_code(city['city'])
    data_manager.sheet_data = sheet_data
    data_manager.update_code()
