import json
from bs4 import BeautifulSoup
from webservice_caller.call_url import call_url
from webservice_caller.call_url import APICallError

class GeocodingAPICaller:
    
    _url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    _key = 'AIzaSyCUM_fu3TzbQtQaBxBCSaKBaP1mGW0k1LU'

    def __init__ (self):
        '''
        Create the location parameters
        '''
        pass

    
    def get_coordinates(self, location):
        '''
        Get the coordinates related to a location 
        '''
        self._location = location
        self._location = self._location.replace(" ", "+")
        url_final = GeocodingAPICaller._url + "address=" + self._location +"+Paris"+ "&key=" + GeocodingAPICaller._key
        response = requests.get(url_final)
        dico = json.loads(response.content)
        try:
            gps_coordinates_dico = dico["results"][0]["geometry"]["location"]
        except IndexError:
            raise APICallError
        except KeyError:
            raise APICallError    
        lat = gps_coordinates_dico["lat"]
        lng = gps_coordinates_dico["lng"]
        return lat, lng
       

    @property
    def location(self):
        return self._location        

class GeocodingAPICallerError(Exception):
    def __init__(self):
        super().__init__('Error occured while calling the Geocoding API')
class AddressNotFoundError(Exception):
    '''
    Raised when the api doesnt find a location
    '''
    def __init__(self, location):
        self.location = location
        super().__init__('{} : location not found'.format(self.location))
