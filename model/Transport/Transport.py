class Transport:
    '''
    Class that all transport inherit from
    '''
    def __init__(self, travel_time, itinerary, is_outside):
        self._travel_time = travel_time
        self._itinerary = itinerary
        self._is_outside = is_outside

    @property
    def travel_time(self):
        return self._travel_time  

    @property
    def travel_time_minute(self):
        return self._travel_time//60

    @property
    def itinerary(self):
        itinerary = self._itinerary.replace(', ','\n')
        return itinerary

    @property
    def is_outside(self):
        return self._is_outside

    def __repr__(self):
        return '{} : {} min \nItinerary:\n {}'.format(self.__class__.__name__, self.travel_time_minute, self.itinerary)

    def __str__(self):
        return '{} : {} min \nItinerary:\n {}'.format(self.__class__.__name__, self.travel_time_minute, self.itinerary)