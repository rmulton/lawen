import json
import requests
import re
from model.Request import Request

class GoogleAPICaller:
    def __init__ (self,url,request):
        self.url = url
        #inital_google_url = 'https://maps.googleapis.com/maps/api/directions/json?'
        self.origin = request.request_from
        #origin = 'Paris'
        self.destination = request.request_to
        #destination = 'Antony'
        self.mode = ['driving','walking','bicycling','transit']
        self.key = 'AIzaSyC2hKozMP10NcIQmqCPesMX0d5nb0lW6cI'
        
    
    def get_transit_times(self):    
        l = {}
        for k in self.mode:
            url_final = self.url + "origin=" + self.origin + "&destination=" + self.destination + "&mode=" + k + "&key=" + self.key
            text = requests.get(url_final)
            dico = json.loads(text.content)          
            l[k] = dico["routes"][0]["legs"][0]["duration"]["value"]
        print(l)

    #def get_possibilities(self):
