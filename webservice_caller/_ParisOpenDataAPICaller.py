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
from webservice_caller.APICallError import APICallError

class _ParisOpenDataAPICaller(TransportAPICaller):
    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self._origin = request.from_x, request.from_y
        self._destination = request.to_x, request.to_y
        self._url = 'https://opendata.paris.fr/api/records/1.0/search/{}'
    

    @property
    def modes(self):
        return self._modes


    def get_nearest_station(self,gps_point):
        '''
        Function that gives the nearest station to one gps point
        '''
        max_walking_distance = 500
        url_gps = self._url + "&geofilter.distance=" + ",".join(str (e) for e in gps_point) + "," + str(max_walking_distance)
        response = requests.get(url_gps)
        self._weather_data_gps = json.loads(response.content)  
        try:
            gps_station = self._weather_data_gps["records"][0]["geometry"]["coordinates"]
        except IndexError:
            raise APICallError
        except KeyError:
            raise APICallError    
        gps_station[1],gps_station[0] = gps_station[0],gps_station[1]
        return gps_station

    def get_subdivision(self):
        '''
        Function that is going to subdivise the total itinerary in smaller ones: real origin, station origin,
        station destination, real destination. The return expected is a list with four GPS coordinates
        '''
        origin_station = _ParisOpenDataAPICaller.get_nearest_station(self,self._origin)
        destination_station = _ParisOpenDataAPICaller.get_nearest_station(self,self._destination)
        return self._origin, origin_station, destination_station, self._destination


    def get_journey(self):    
        '''
        Use the get_subdivision function to split the journey to three parts: the walking to the station,
        the driving/biking from station to station, and the walking from station to destination.
        Creates the transportation objects containing each its time and itinerary
        '''
        origin, origin_station, destination_station, destination = _ParisOpenDataAPICaller.get_subdivision(self)

        origin_to_station = Request(origin[0], origin[1], origin_station[0], origin_station[1])
        station_to_station = Request(origin_station[0], origin_station[1], destination_station[0], destination_station[1])
        station_to_destination = Request(destination_station[0], destination_station[1], destination[0], destination[1])

        caller_origin_to_station = GoogleAPICaller(origin_to_station)
        possibilities_origin_to_sation = caller_origin_to_station.get_possibilities()

        caller_station_to_station = GoogleAPICaller(station_to_station)
        possibilities_station_to_station = caller_station_to_station.get_possibilities()

        caller_station_to_destination = GoogleAPICaller(station_to_destination)
        possibilities_station_to_destination = caller_station_to_destination.get_possibilities()
        
        return possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination

    def get_times(self):    
        '''
        Get the total time by adding the walking and the driving/biking times
        '''
        travel_times = {}
        for mode_name, mode_class in self._modes.items():
            possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination = self.get_journey()
            walking_time = possibilities_origin_to_sation.transports['walking'].travel_time + possibilities_station_to_destination.transports['walking'].travel_time
            mode_time = possibilities_station_to_station.transports[list(self._modes.keys())[0]].travel_time 
            travel_time = walking_time + mode_time
            travel_times[mode_name] = travel_time
        return travel_times

    def get_itineraries(self):    
        '''
        Get the total itinerary by adding the walking and the driving/biking itineraries
        '''
        itinerairies = {}
        for mode_name, mode_class in self._modes.items():
            possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination = _ParisOpenDataAPICaller.get_journey(self)
            walking_to_station = possibilities_origin_to_sation.transports['walking'].itinerary
            station_to_station = possibilities_station_to_station.transports[list(self._modes.keys())[0]].itinerary
            walking_to_destination = possibilities_station_to_destination.transports['walking'].itinerary
            itinerary = "{} Take your {} from the station \n {} Park your {} in the station \n{}"
            itinerary = itinerary.format(walking_to_station, list(self._modes.values())[0].__name__, station_to_station, list(self._modes.values())[0].__name__, walking_to_destination)
            itinerairies[mode_name] = itinerary
        return itinerairies

