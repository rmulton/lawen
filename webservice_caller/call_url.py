import requests

def call_url(url):
    '''
    Handle api calls and their frequent errors
    '''
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        raise APICallError
    except requests.exceptions.ConnectionError as e:
        raise APICallError

class APICallError(Exception):
    def __init__(self):
        super().__init__('Error occured while calling an API')