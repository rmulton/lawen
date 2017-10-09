class Request:
    def __init__(self, request_from, request_to):
        self._request_from = request_from
        self._request_to = request_to

    @property
    def request_from(self):
        return self._request_from

    @property
    def request_to(self):
        return self._request_to
