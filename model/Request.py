def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def check_float(name, string):
    if not is_float(string) or len(string)==0:
        raise InvalidRequestError(name, string)

def check_inside_paris(name, coordinate):
    x = coordinate[0]
    y = coordinate[1]
    if not(x<48.897749 and x>48.816999 and y<2.410515 and y>2.238510):
        raise NotInParisRequestError(name, coordinate)

class Request():

    def __init__(self, from_x, from_y, to_x, to_y):
        self._from_x = from_x
        self._from_y = from_y
        self._to_x = to_x
        self._to_y = to_y
        self.check_request()

        '''
        ex: 48.7593013, 2.3023274, 48.857296, 2.352394
        '''
    
    def check_input_is_coordinate(self):
        for field_name, field_value in self.inputs.items():
            check_float(field_name, field_value)

    def check_coordinate_inside_paris(self):
        for name, coordinate in self.coordinates.items():
            check_inside_paris(name, coordinate)

    def check_request(self):
        # Check that it is a GPS coordinate
        self.check_input_is_coordinate()
        # Check that the coordinate is inside Paris
        self.check_coordinate_inside_paris()
        
        
    @property
    def from_x(self):
        return float(self._from_x)

    @property
    def from_y(self):
        return float(self._from_y)

    @property
    def to_x(self):
        return float(self._to_x)

    @property
    def to_y(self):
        return float(self._to_y)

    @property
    def inputs(self):
        return self.__dict__

    @property
    def origin(self):
        return self.from_x, self.from_y

    @property
    def destination(self):
        return self.to_x, self.to_y

    @property
    def coordinates(self):
        return {'origin': self.origin, 'destination': self.destination}

class InvalidRequestError(Exception):
    def __init__(self, field_name, value):
        self.value = value
        self.field_name = field_name
        super().__init__('{} is set to \'{}\' : not convertible to float'.format(self.field_name, self.value))

class NotInParisRequestError(Exception):
    def __init__(self, field_name, value):
        self.value = value
        self.field_name = field_name
        super().__init__('{} is set to \'{}\' : GPS coordinate must be inside Paris'.format(self.field_name, self.value))
       