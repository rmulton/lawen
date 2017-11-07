import json
import requests
from bs4 import BeautifulSoup
from webservice_caller.APICallError import APICallError

class GeocodingAPICaller:
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    key = 'AIzaSyCUM_fu3TzbQtQaBxBCSaKBaP1mGW0k1LU'

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
        url_final = GeocodingAPICaller.url + "address=" + self._location +"+Paris"+ "&key=" + GeocodingAPICaller.key
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

class AddressNotFoundError(Exception):
    '''
    Raised when the api doesnt find a location
    '''
    def __init__(self, location):
        self.location = location
        super().__init__('{} : location not found'.format(self.location))
