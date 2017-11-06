from model.Request import Request
from webservice_caller.GeocodingAPICaller import GeocodingAPICaller

class UserRequest():
    def __init__(self, from_location, to_location):
        self._from_location = from_location
        self._to_location = to_location
        self._coordinates = self.create_request()

    @property
    def coordinates(self):
        return self._coordinates

    def create_request(self):
        geocoding_caller = GeocodingAPICaller()
        from_x, from_y = geocoding_caller.get_coordinates(self._from_location)
        to_x, to_y = geocoding_caller.get_coordinates(self._to_location)
        # return Request(from_x, from_y, to_x, to_y)
        return Request(48.84, 2.4, 48.85, 2.4)