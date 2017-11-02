import math

class Possibilities:
    '''
    Represents the different ways to go from A to B
    For now we check using public transportation, cycling, walking, driving, using Autolib and Velib
    '''
    def __init__(self, weather, transports):
        self._weather = weather
        # Remove some transportations regarding the weather
        self._set_transports(transports)
        # Choose what transportation to suggest to the user
        self.choose_best_transport()
    
    @property
    def weather(self):
        return self._weather

    @property
    def transports(self):
        return self._transports

    @property
    def best_transport(self):
        return self._best_transport

    def _set_transports(self, transports):
        '''
        If it is raining, remove the transportation which are mostly outside
        '''
        if self.weather == 'rain':
            transports = avoid_being_outside(transports)
        self._transports = transports
    
    def choose_best_transport(self):
        if len(self.transports) == 0:
            print('Error')
        best_so_far = self.transports[next(iter(self.transports))]
        for transport_name, transport in self.transports.items():
            if transport.travel_time<best_so_far.travel_time:
                best_so_far = transport
        self._best_transport = best_so_far
        


def avoid_being_outside(transports):
    new_dict = transports
    for name, transport in transports.items():
        if transport.is_outside:
            new_dict[name]
    return new_dict
