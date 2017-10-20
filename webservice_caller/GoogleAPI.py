import json
import requests
import re
from model.Transport.Walk import Walk
from model.Transport.PublicTransport import PublicTransport
from model.Transport.Drive import Drive
from model.Transport.Bicycle import Bicycle
from model.Possibilities import Possibilities

class GoogleAPICaller:
    
    url = 'https://maps.googleapis.com/maps/api/directions/json?'
    key = 'AIzaSyC2hKozMP10NcIQmqCPesMX0d5nb0lW6cI'

    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self.origin = request.from_x, request.from_y
        self.destination = request.to_x, request.to_y
        self.modes = {'driving':Drive,'walking':Walk,'bicycling':Bicycle,'transit':PublicTransport}
        
        
    
    def get_possibilities(self):    
        '''
        Get the different times related to the travel modes and returns 
        a list of objects corresponding to each travel mode'
        '''
        possibilities = {}
        try:
            for mode, mode_class in self.modes.items():
                url_final = GoogleAPICaller.url + "origin=" + ",".join(str (e) for e in self.origin) + "&destination=" + ",".join(str(f) for f in self.destination) + "&mode=" + mode + "&key=" + GoogleAPICaller.key
                response = requests.get(url_final)
                dico = json.loads(response.content)  
                travel_time = dico["routes"][0]["legs"][0]["duration"]["value"]
                possibilities[mode] = mode_class(travel_time)
            return Possibilities('rain', possibilities)
        except IndexError:
            print("Problem with the origin or destination address (not found)")
        except requests.exceptions.ConnectionError:
            print("Are you in Bouygues? Because you have no internet connection. Go out and try again")  



                
