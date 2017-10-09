class Transport:
    def __init__(self, travel_time):
        self._travel_time = travel_time
    
    @property
    def travel_time(self):
        return self._travel_time