from model.Transport.Transport import Transport

class Autolib(Transport):
    '''
    Class to store autolib informations
    '''
    def __init__(self, travel_time, itinerary):
        super().__init__(travel_time, itinerary, False)
    
    