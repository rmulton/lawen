from model.Transport.Transport import Transport

class Walk(Transport):
    '''
    Class to store walking informations
    '''
    def __init__(self, travel_time, itinerary):
        super().__init__(travel_time, itinerary, True)

