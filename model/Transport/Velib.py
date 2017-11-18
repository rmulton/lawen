from model.Transport.Transport import Transport

class Velib(Transport):
    '''
    Class to store velib informations
    '''
    def __init__(self, travel_time, itinerary):
        super().__init__(travel_time, itinerary, True)
