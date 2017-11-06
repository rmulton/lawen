import math

class Possibilities:
    '''
    Represents the different ways to go from A to B
    For now we check using public transportation, cycling, walking, driving, using Autolib and Velib
    '''
    def __init__(self, transports, is_raining=False):
        self._is_raining = is_raining
        # Remove some transportations regarding the weather
        self._set_transports(transports)
    
    @property
    def is_raining(self):
        return self._is_raining

    @property
    def transports(self):
        return self._transports

    @property
    def best_transport(self):
        self.choose_best_transport()
        return self._best_transport

    def _set_transports(self, transports):
        '''
        If it is raining, remove the transportation which are mostly outside
        '''
        if self.is_raining == True:
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
