class Proposition:
    def __init__(self, transportation_options, ranked_chosen_options):
        self._transportation_options = transportation_options
        self._ranked_chosen_options = ranked_chosen_options
    
    @property
    def transportation_options(self):
        return self._transportation_options
    
    @property
    def ranked_chosen_options(self):
        return self._ranked_chosen_options