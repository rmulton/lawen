class APICallError(Exception):
    def __init__(self):
        super().__init__('Error occured while calling an API.')