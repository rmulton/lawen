import json
import re
from bs4 import BeautifulSoup
from model.Transport.Walk import Walk
from model.Transport.PublicTransport import PublicTransport
from model.Transport.Drive import Drive
from model.Transport.Bicycle import Bicycle
from model.Possibilities import Possibilities
from webservice_caller.TransportAPICaller import TransportAPICaller
from webservice_caller.call_url import call_url, APICallError

class GoogleAPICaller(TransportAPICaller):
    
    _url = 'https://maps.googleapis.com/maps/api/directions/json?'
    _key = 'AIzaSyCqgwlzgUDYYF7xnePerJZaapgUWmyGYjc'

    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self._origin = request.from_x, request.from_y
        self._destination = request.to_x, request.to_y
        self._modes = {'driving':Drive,'walking':Walk,'bicycling':Bicycle,'transit':PublicTransport}

    @property
    def modes(self):
        return self._modes

    def get_times(self):    
        '''
        Get the different times related to the travel modes and returns 
        a list of objects corresponding to each travel mode'
        '''
        times = {}
    
        for mode, mode_class in self._modes.items():
            url_final = GoogleAPICaller._url + "origin=" + ",".join(str (e) for e in self._origin) + "&destination=" + ",".join(str(f) for f in self._destination) + "&mode=" + mode + "&key=" + GoogleAPICaller._key
            response = call_url(url_final)
            data = json.loads(response.content)  
            try:
                travel_time = data["routes"][0]["legs"][0]["duration"]["value"]
            except IndexError:
                raise APICallError
            except KeyError:
                raise APICallError
            times[mode] = travel_time
        return times
    

    def get_itineraries(self):
        '''
        Get the different itineraries related to the travel modes
        '''
        itineraries = {}
        for mode, mode_class in self._modes.items():
            url_final = GoogleAPICaller._url + "origin=" + ",".join(str (e) for e in self._origin) + "&destination=" + ",".join(str(f) for f in self._destination) + "&mode=" + mode + "&key=" + GoogleAPICaller._key
            response = call_url(url_final)
            data = json.loads(response.content)  
            try:
                instruction = data["routes"][0]["legs"][0]["steps"]
            except IndexError:
                raise APICallError
            except KeyError:
                raise APICallError    
            itinerary = ""
            for i in range(len(instruction)):
                itinerary += instruction[i]["html_instructions"] + ", "
            clean_itinerary = BeautifulSoup(itinerary,"html.parser").text
            itineraries[mode] = clean_itinerary  
        return itineraries  
