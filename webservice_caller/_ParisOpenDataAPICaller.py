import json
import requests
import re
from webservice_caller.GoogleAPICaller import GoogleAPICaller
from model.Request import Request
from model.Transport.Velib import Velib
from model.Transport.Bicycle import Bicycle
from model.Transport.Drive import Drive
from model.Transport.Autolib import Autolib
from model.Possibilities import Possibilities
from webservice_caller.TransportAPICaller import TransportAPICaller

class _ParisOpenDataAPICaller(TransportAPICaller):
    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self.origin = request.from_x, request.from_y
        self.destination = request.to_x, request.to_y
        self.url = 'https://opendata.paris.fr/api/records/1.0/search/{}'
    
    def get_nearest_station(self,gps_point):
        '''
        Function that gives the nearest station to one gps point
        '''
        max_walking_distance = 500
        url_gps = self.url + "&geofilter.distance=" + ",".join(str (e) for e in gps_point) + "," + str(max_walking_distance)
        response = requests.get(url_gps)
        self._weather_data_gps = json.loads(response.content)  
        gps_station = self._weather_data_gps["records"][0]["geometry"]["coordinates"]
        gps_station[1],gps_station[0] = gps_station[0],gps_station[1]
        return gps_station

    def get_subdivision(self):
        '''
        Function that is going to subdivise the total itinerary in smaller ones: real origin, station origin,
        station destination, real destination. The return expected is a list with four GPS coordinates
        '''
        origin_station = _ParisOpenDataAPICaller.get_nearest_station(self,self.origin)
        destination_station = _ParisOpenDataAPICaller.get_nearest_station(self,self.destination)
        return self.origin, origin_station, destination_station, self.destination


    def get_journey(self):    
        '''
        Get the time related to the travel mode and returns 
        an object created by the corresponding class'
        '''
        origin, origin_station, destination_station, destination = _ParisOpenDataAPICaller.get_subdivision(self)

        origin_to_station = Request(str(origin[0]), str(origin[1]), str(origin_station[0]), str(origin_station[1]))
        station_to_station = Request(str(origin_station[0]), str(origin_station[1]), str(destination_station[0]), str(destination_station[1]))
        station_to_destination = Request(str(destination_station[0]), str(destination_station[1]), str(destination[0]), str(destination[1]))

        caller_origin_to_station = GoogleAPICaller(origin_to_station)
        possibilities_origin_to_sation = caller_origin_to_station.get_possibilities()

        caller_station_to_station = GoogleAPICaller(station_to_station)
        possibilities_station_to_station = caller_station_to_station.get_possibilities()

        caller_station_to_destination = GoogleAPICaller(station_to_destination)
        possibilities_station_to_destination = caller_station_to_destination.get_possibilities()
        
        return possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination

    def get_times(self):    
        travel_times = {}
        for mode_name, mode_class in self.modes.items():
            possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination = self.get_journey()
            walking_time = possibilities_origin_to_sation.transports['walking'].travel_time + possibilities_station_to_destination.transports['walking'].travel_time
            mode_time = possibilities_station_to_station.transports[list(self.modes.keys())[0]].travel_time 
            travel_time = walking_time + mode_time
            travel_times[mode_name] = travel_time
        return travel_times

    def get_itineraries(self):    
        itinerairies = {}
        for mode_name, mode_class in self.modes.items():
            possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination = _ParisOpenDataAPICaller.get_journey(self)
            walking_to_station = possibilities_origin_to_sation.transports['walking'].itinerary
            station_to_station = possibilities_station_to_station.transports[list(self.modes.keys())[0]].itinerary
            walking_to_destination = possibilities_station_to_destination.transports['walking'].itinerary
            itinerary = walking_to_station + "Take your" + str([list(self.modes.values())[0]]) + "from the station \n" + station_to_station + "Park your" + str([list(self.modes.values())[0]]) + "in the station \n"+ walking_to_destination
            itinerairies[mode_name] = itinerary
        return itinerairies

