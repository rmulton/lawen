class Transport:
    def __init__(self, travel_time, is_outside):
        self._travel_time = travel_time
        self._is_outside = is_outside

    @property
    def travel_time(self):
        return self._travel_time

    @property
    def is_outside(self):
        return self._is_outside

    def __repr__(self):
        return '{} : {}s'.format(self.__class__.__name__, self.travel_time)

    def __str__(self):
        return '{} : {}s'.format(self.__class__.__name__, self.travel_time)