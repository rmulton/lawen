import json
import requests
from bs4 import BeautifulSoup

class GeocodingAPICaller:
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    key = 'AIzaSyCUM_fu3TzbQtQaBxBCSaKBaP1mGW0k1LU'

    def __init__ (self, location):
        '''
        Create the location parameters
        '''
        self._location = location

    def get_coordinates(self):
        '''
        Get the coordinates related to a location 
        '''
        try:
            self._location = self._location.replace(" ", "+")
            url_final = GeocodingAPICaller.url + "address=" + self._location +"+Paris"+ "&key=" + GeocodingAPICaller.key
            response = requests.get(url_final)
            dico = json.loads(response.content)  
            gps_coordinates_dico = dico["results"][0]["geometry"]["location"]
            lat = gps_coordinates_dico["lat"]
            lng = gps_coordinates_dico["lng"]
            return lat, lng
        except IndexError:
            print("Google n'a pas trouve l'addresse")

        @property
        def location(self):
            return self._location
