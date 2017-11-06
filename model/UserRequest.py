from model.Request import Request
class UserRequest():
    def __init__(self, from_location, to_location):
        self._from_location = from_location
        self._to_location = to_location
        self._coordinates = self.create_request()

    @property
    def coordinates(self):
        return self._coordinates
    
    def create_request(self):
        return Request('48.83', '2.4', '48.84', '2.4')