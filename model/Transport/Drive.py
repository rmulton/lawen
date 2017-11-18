from model.Transport.Transport import Transport

class Drive(Transport):
    '''
    Class to store driving informations
    '''
    def __init__(self, travel_time, itinerary):
        super().__init__(travel_time, itinerary, False)
