from model.Request import Request
from webservice_caller.GeocodingAPICaller import GeocodingAPICaller, AddressNotFoundError, GeocodingAPICallerError

class UserRequest():
    def __init__(self, from_location, to_location):
        self._from_location = from_location
        self._to_location = to_location
        self.check_locations()
        self._coordinates = self.create_request()

    def __str__(self):
        return 'Go from {} to {}'.format(self._from_location, self._to_location)
    @property
    def coordinates(self):
        return self._coordinates

    def check_locations(self):
        if not len(self._from_location)>0:
            raise EmptyFieldError('_from_location')
        if not len(self._to_location)>0:
            raise EmptyFieldError('_to_location')

    def create_request(self):
        geocoding_caller = GeocodingAPICaller()
        try:
            from_x, from_y = geocoding_caller.get_coordinates(self._from_location)
        except AddressNotFoundError as e:
            raise LocationNotFoundError('_from_location', self._from_location)
        except GeocodingAPICallerError as e:
            raise GeocodingAPICallerError
        try:
            to_x, to_y = geocoding_caller.get_coordinates(self._to_location)
        except AddressNotFoundError as e:
            raise LocationNotFoundError('_to_location', self._to_location)
        except GeocodingAPICaller as e:
            raise GeocodingAPICallerError
        return Request(from_x, from_y, to_x, to_y)

class LocationNotFoundError(Exception):
    '''
    Raised when an input is not found by the geocoding api
    '''
    def __init__(self, field_name, value):
        self.value = value
        self.field_name = field_name
        super().__init__('{} is set to \'{}\' : Location not found'.format(self.field_name, self.value))

class EmptyFieldError(Exception):
    '''
    Raised when an input is empty
    '''
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__('{} is empty'.format(self.field_name))

