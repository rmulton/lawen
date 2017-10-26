from model.Transport.Transport import Transport

class Autolib(Transport):
    def __init__(self, travel_time, itinerary):
        super().__init__(travel_time, itinerary, False)
    
    