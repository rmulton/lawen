import json
import requests
from bs4 import BeautifulSoup

class GeocodingAPICaller:
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    key = 'AIzaSyCUM_fu3TzbQtQaBxBCSaKBaP1mGW0k1LU'

    def __init__ (self):
        '''
        Create the location parameters
        '''
        pass

    
    def get_coordinates(self, _location):
        '''
        Get the coordinates related to a location 
        '''
        self._location = _location
        try:
            self._location = self._location.replace(" ", "+")
            url_final = GeocodingAPICaller.url + "address=" + self._location +"+Paris"+ "&key=" + GeocodingAPICaller.key
            response = requests.get(url_final)
            dico = json.loads(response.content)
            if len(dico["results"]) == 0:
                raise AddressNotFoundError
            else:    
                gps_coordinates_dico = dico["results"][0]["geometry"]["location"]
                lat = gps_coordinates_dico["lat"]
                lng = gps_coordinates_dico["lng"]
                return lat, lng
        except ConnectionError:
            print("connection error")

    @property
    def location(self):
        return self._location        