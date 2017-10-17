import math

class Possibilities:
    def __init__(self, weather, transports):
        self._weather = weather
        self._set_transports(transports)
    
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
        if self.weather == 'rain':
            transports = avoid_being_outside(transports)
        self._transports = transports
    
    def choose_best_transport(self):
        if len(self.transports) == 0:
            print('Error')
        best_so_far = self.transports[0]
        for transport in self.transports:
            if transport.travel_time<best_so_far.travel_time:
                best_so_far = transport
        self._best_transport = best_so_far
        


def avoid_being_outside(transports):
    for transport in transports:
        if transport.is_outside:
            transports.remove(transport)
    return transports
