def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def check_float(name, string):
    if not is_float(string) or len(string)==0:
        raise InvalidRequestError(name, string)

class Request():

    def __init__(self, from_x, from_y, to_x, to_y):
        self._from_x = from_x
        self._from_y = from_y
        self._to_x = to_x
        self._to_y = to_y
        self.check_request()
    
    def check_request(self):
        for field_name, field_value in self.__dict__.items():
            check_float(field_name, field_value)
        
    @property
    def from_x(self):
        return self._from_x

    @property
    def from_y(self):
        return self._from_y

    @property
    def to_x(self):
        return self._to_x

    @property
    def to_y(self):
        return self._to_y

class InvalidRequestError(Exception):
    def __init__(self, field_name, value):
        self.value = value
        self.field_name = field_name
        super().__init__('{} is set to \'{}\' : not convertible to float'.format(self.field_name, self.value))
        