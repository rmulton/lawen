from model.Transport.Transport import Transport

class Bicycle(Transport):
    def __init__(self, travel_time, itinerary):
        super().__init__(travel_time, itinerary, True)
