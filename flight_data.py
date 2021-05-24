class FlightData:
    def __init__(self, price, airline, from_city, to_city, from_airport, to_airport,
                 from_date, return_date, stop_over=0, via_city=''):
        self.price = price
        self.airline = airline
        self.from_city = from_city
        self.to_city = to_city
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.from_date = from_date
        self.return_date = return_date
        self.stop_over = stop_over
        self.via_city = via_city
        print(f'{to_city}: Rp {price}')
