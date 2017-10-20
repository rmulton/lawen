import json
import requests
import re
from model.Transport.Walk import Walk
from model.Transport.PublicTransport import PublicTransport

class GoogleAPICaller:
    
    url = 'https://maps.googleapis.com/maps/api/directions/json?'
    key = 'AIzaSyC2hKozMP10NcIQmqCPesMX0d5nb0lW6cI'

    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self.origin = request.request_from
        self.destination = request.request_to
        self.modes = ['driving','walking','bicycling','transit']
        
        
    
    def get_times(self):    
        '''
        Get the different times related to the travel modes and returns 
        a list of objects corresponding to each travel mode'
        '''
        possibilities = []
        try:
            for mode in self.modes:
                url_final = GoogleAPICaller.url + "origin=" + ",".join(str (e) for e in self.origin) + "&destination=" + ",".join(str(f) for f in self.destination) + "&mode=" + mode + "&key=" + GoogleAPICaller.key
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
        except IndexError:
            print("Problem with the origin or destination address (not found)")
        except requests.exceptions.ConnectionError:
            print("Are you in Bouygues? Because you have no internet connection. Go out and try again")  



                
