class Proposition:
    def __init__(self, choice):
        self._choice = choice
    
    @property
    def choice(self):
        return self._choice