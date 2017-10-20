from model.Transport.Transport import Transport

class Drive(Transport):
    def __init__(self, travel_time):
        super().__init__(travel_time, True)
