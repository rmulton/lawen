from webservice_caller.GoogleAPICaller import GoogleAPICaller
from webservice_caller.VelibAPICaller import VelibAPICaller
from webservice_caller.AutolibAPICaller import AutolibAPICaller
from webservice_caller.WeatherAPICaller import WeatherAPICaller

from model.Possibilities import Possibilities
import time

from webservice_caller.call_url import APICallError

class AllAPICaller:
    '''
    Used as an interface to get the possible itiniraries as a whole, using Possibilities object
    '''
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
        try:
            # Get the transportation means
            transports = {}
            for api_name, api_caller in self.api_callers.items():
                caller_possibilities = api_caller.get_possibilities()
                caller_transports = caller_possibilities.transports
                transports.update(caller_transports)

            # Get the weather
            weather_caller = WeatherAPICaller(time.time())
            rain_mm = weather_caller.rain
            if rain_mm==0:
                is_raining = False
            else:
                is_raining = True
            
            # Create the Possibilities object that contains information to display
            possiblities = Possibilities(transports, is_raining=is_raining)
            return possiblities
        except APICallError as e:
            raise MainCallerError

class MainCallerError(Exception):
    def __init__(self):
        super().__init__('Error occured while calling an API')