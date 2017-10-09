class TransportationOptions:
    def __init__(self, request, weather, public_transportation, autolib, velib, walk):
        self._request = request
        self._weather = weather
        self._public_tranportation = public_transportation
        self._autolib = autolib
        self._velib = velib
        self._walk = walk
    
    @property
    def request(self):
        return self._request
    
    @property
    def weather(self):
        return self._weather

    @property
    def public_transportation(self):
        return self._public_tranportation

    @property
    def velib(self):
        return self._velib

    @property
    def autolib(self):
        return self._autolib

    @property
    def walk(self):
        return self._walk
