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

    def _set_transports(self, transports):
        if self.weather == 'rain':
            transports = avoid_being_outside(transports)
        self._transports = transports

def avoid_being_outside(transports):
    outside_transports = ['velib', 'walk']
    for key in transports.keys():
        if key in outside_transports:
            transports.pop(key)
    return transports
