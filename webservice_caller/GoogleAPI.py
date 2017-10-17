import json
import requests
import re
from model.Transport.Walk import Walk
from model.Transport.PublicTransport import PublicTransport

class GoogleAPICaller:
    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self.url = 'https://maps.googleapis.com/maps/api/directions/json?'
        self.origin = request.request_from
        self.destination = request.request_to
        self.modes = ['driving','walking','bicycling','transit']
        self.key = 'AIzaSyC2hKozMP10NcIQmqCPesMX0d5nb0lW6cI'
        
    
    def get_possibilities(self):    
        '''
        Get the different times related to the travel modes and returns 
        a list of objects corresponding to each travel mode'
        '''
        possibilities = []
        for mode in self.modes:
            url_final = self.url + "origin=" + ",".join(str (e) for e in self.origin) + "&destination=" + ",".join(str(f) for f in self.destination) + "&mode=" + mode + "&key=" + self.key
            response = requests.get(url_final)
            dico = json.loads(response.content)          
            travel_time = dico["routes"][0]["legs"][0]["duration"]["value"]
            if mode == 'walking':
                transport = Walk(travel_time)
            elif mode == 'transit':
                transport = PublicTransport(travel_time)
            else:
                continue         
            possibilities.append(transport)    
        return(possibilities)
                
