import json
import requests
import re
from webservice_caller.GoogleAPICaller import GoogleAPICaller
from model.Request import Request
from model.Transport.Autolib import Autolib
from model.Transport.Velib import Velib

class ParisOpenDataAPICaller:
    url_mode = {
        'velib': '?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=bonus&facet=status&facet=contract_name',
        'autolib': '?dataset=autolib-disponibilite-temps-reel&facet=charging_status&facet=kind&facet=postal_code&facet=slots&facet=status&facet=subscription_status'
    }
    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self.origin = request.from_x, request.from_y
        self.destination = request.to_x, request.to_y
        self.url = 'https://opendata.paris.fr/api/records/1.0/search/{}'
        self.modes = {
            'velib': Velib,
            'autolib': Autolib
        }
    
    def get_times(self):
        for mode_name, mode_class in self.modes.items():
            self.url = self.url.format(ParisOpenDataAPICaller.url_mode[mode_name])
            travel_time = self.get_time()
            times[mode] = travel_time
            return times


    def get_itineraries(self):
        for mode_name, mode_class in self.modes.items():
            self.url = self.url.format(ParisOpenDataAPICaller.url_mode[mode_name])
            itinerary = self.get_itinerary()
            itineraries[mode] = itinerary
            return itineraries

    def get_nearest_station(self,gps_point):
        '''
        Function that gives the nearest station to one gps point
        '''
        max_walking_distance = 500
        url_gps = self.url + "&geofilter.distance=" + ",".join(str (e) for e in gps_point) + "," + str(max_walking_distance)
        response = requests.get(url_gps)
        dico_gps = json.loads(response.content)  
        gps_station = dico_gps["records"][0]["geometry"]["coordinates"]
        gps_station[1],gps_station[0] = gps_station[0],gps_station[1]
        return gps_station

    def get_subdivision(self):
        '''
        Function that is going to subdivise the total itinerary in smaller ones: real origin, station origin,
        station destination, real destination. The return expected is a list with four GPS coordinates
        '''
        origin_station = ParisOpenDataAPICaller.get_nearest_station(self,self.origin)
        destination_station = ParisOpenDataAPICaller.get_nearest_station(self,self.destination)
        return self.origin, origin_station, destination_station, self.destination


    def get_journey(self):    
        '''
        Get the time related to the travel mode and returns 
        an object created by the corresponding class'
        '''
        origin, origin_station, destination_station, destination = _SharedAPICaller.get_subdivision(self)

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

    def get_time(self):    

        possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination = _SharedAPICaller.get_journey(self)
        walking_time = possibilities_origin_to_sation.transports['walking'].travel_time + possibilities_station_to_destination.transports['walking'].travel_time
        mode_time = possibilities_station_to_station.transports[self.mode].travel_time 
        travel_time = walking_time + mode_time
        return travel_time

    def get_itinerary(self):    
        possibilities_origin_to_sation, possibilities_station_to_station, possibilities_station_to_destination = _SharedAPICaller.get_journey(self)
        walking_to_station = possibilities_origin_to_sation.transports['walking'].itinerary
        station_to_station = possibilities_station_to_station.transports[self.mode].itinerary
        walking_to_destination = possibilities_station_to_destination.transports['walking'].itinerary
        instructions = walking_to_station + station_to_station + walking_to_destination
        return instructions
