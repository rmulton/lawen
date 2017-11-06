from webservice_caller.GoogleAPICaller import GoogleAPICaller
from webservice_caller.VelibAPICaller import VelibAPICaller
from webservice_caller.AutolibAPICaller import AutolibAPICaller
from webservice_caller.WeatherAPICaller import WeatherAPICaller

from model.Possibilities import Possibilities
import time

class AllAPICaller:
    def __init__(self, request):
        self._request = request
        self._api_callers = {
            'google': GoogleAPICaller(self.request),
            'velib': VelibAPICaller(self.request),
            'autolib': AutolibAPICaller(self.request)
        }
    
    @property
    def request(self):
        return self._request

    @property
    def api_callers(self):
        return self._api_callers

    def get_possibilities(self):
        # Get the transportation means
        transports = {}
        for api_name, api_caller in self.api_callers.items():
            caller_possibilities = api_caller.get_possibilities()
            caller_transports = caller_possibilities.transports
            transports.update(caller_transports)

        # Get the weather
        weather_caller = WeatherAPICaller(time.time())
        # weather = weather_caller.rain
        weather = 'rain'
        
        # Create the Possibilities object that contains information to display
        possiblities = Possibilities('rain', transports)
        return possiblities

            