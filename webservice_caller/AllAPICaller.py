from webservice_caller.GoogleAPICaller import GoogleAPICaller
from webservice_caller.VelibAPICaller import VelibAPICaller
from webservice_caller.AutolibAPICaller import AutolibAPICaller

from model.Possibilities import Possibilities

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
        transports = {}
        for api_name, api_caller in self.api_callers.items():
            caller_possibilities = api_caller.get_possibilities()
            caller_transports = caller_possibilities.transports
            transports.update(caller_transports)
        possiblities = Possibilities('rain', transports)
        return possiblities

            