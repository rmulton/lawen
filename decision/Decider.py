class Decider:
    def __init__(self, possibilities):
        self._possibilities = possibilities
        self.decide_which_transport()

    @property
    def possibilities(self):
        return self._possibilities
    
    def decide_which_transport(self):

        possibilities = self.possibilities
        weather = possibilities.weather
        transports = possibilities.tranports

        if weather == "rain":
            transports = 
        

