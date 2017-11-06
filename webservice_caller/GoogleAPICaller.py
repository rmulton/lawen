import json
import requests
import re
from bs4 import BeautifulSoup
from model.Transport.Walk import Walk
from model.Transport.PublicTransport import PublicTransport
from model.Transport.Drive import Drive
from model.Transport.Bicycle import Bicycle
from model.Possibilities import Possibilities
from webservice_caller.TransportAPICaller import TransportAPICaller

class GoogleAPICaller(TransportAPICaller):
    
    url = 'https://maps.googleapis.com/maps/api/directions/json?'
    key = 'AIzaSyC2hKozMP10NcIQmqCPesMX0d5nb0lW6cI'

    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self._origin = request.from_x, request.from_y
        self._destination = request.to_x, request.to_y
        self._modes = {'driving':Drive,'walking':Walk,'bicycling':Bicycle,'transit':PublicTransport}
        
    @property
    def origin(self):
        return self._origin

    @property
    def destination(self):
        return self._destination

    @property
    def modes(self):
        return self._modes



    def get_times(self):    
        '''
        Get the different times related to the travel modes and returns 
        a list of objects corresponding to each travel mode'
        '''
        times = {}
        try:
            for mode, mode_class in self._modes.items():
                url_final = GoogleAPICaller.url + "origin=" + ",".join(str (e) for e in self._origin) + "&destination=" + ",".join(str(f) for f in self._destination) + "&mode=" + mode + "&key=" + GoogleAPICaller.key
                response = requests.get(url_final)
                self._weather_data = json.loads(response.content)  
                travel_time = self._weather_data["routes"][0]["legs"][0]["duration"]["value"]
                times[mode] = travel_time
            return times
        except IndexError:
            print("Problem with the origin or destination address (not found)")
        except requests.exceptions.ConnectionError:
            print("Are you in Bouygues? Because you have no internet connection. Go out and try again")  
    

    def get_itineraries(self):
        '''
        Get the different itineraries related to the travel modes
        '''
        itineraries = {}
        for mode, mode_class in self._modes.items():
            url_final = GoogleAPICaller.url + "origin=" + ",".join(str (e) for e in self._origin) + "&destination=" + ",".join(str(f) for f in self._destination) + "&mode=" + mode + "&key=" + GoogleAPICaller.key
            response = requests.get(url_final)
            self._weather_data = json.loads(response.content)  
            instruction = self._weather_data["routes"][0]["legs"][0]["steps"]
            itinerary = ""
            for i in range(len(instruction)):
                itinerary += instruction[i]["html_instructions"] + ", "
            clean_itinerary = BeautifulSoup(itinerary,"html.parser").text
            itineraries[mode] = clean_itinerary  
        return itineraries  
