import requests

def call_url(url):
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        raise APICallError

class APICallError(Exception):
    def __init__(self):
        super().__init__('Error occured while calling an API')