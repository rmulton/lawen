import json
import requests
import re
from webservice_caller.GoogleAPI import GoogleAPICaller
from model.Request import Request

class _SharedAPICaller:

    def __init__ (self, request):
        '''
        Create the different parameters that we will need for the API url
        '''
        self.origin = request.request_from
        self.destination = request.request_to
        self.url = 'https://opendata.paris.fr/api/records/1.0/search/{}'
        self.mode = ""
        

    
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
        origin_station = _SharedAPICaller.get_nearest_station(self,self.origin)
        destination_station = _SharedAPICaller.get_nearest_station(self,self.destination)
        gps_list = [self.origin, origin_station, destination_station, self.destination]
        return gps_list    


    def get_time(self):    
        '''
        Get the time related to the travel mode and returns 
        an object created by the corresponding class'
        '''
        gps_list = _SharedAPICaller.get_subdivision(self)

        origin_to_station = Request(gps_list[0],gps_list[1])
        station_to_station = Request(gps_list[1],gps_list[2])
        station_to_destination = Request(gps_list[2],gps_list[3])

        caller_origin_to_station = GoogleAPICaller(origin_to_station)
        possibilities_origin_to_sation = caller_origin_to_station.get_possibilities()
        caller_station_to_station = GoogleAPICaller(station_to_station)
        possibilities_station_to_station = caller_station_to_station.get_possibilities()
        caller_station_to_destination = GoogleAPICaller(station_to_destination)
        possibilities_station_to_destination = caller_station_to_destination.get_possibilities()
        
        travel_time = possibilities_origin_to_sation['walking'].travel_time + possibilities_station_to_station[self.mode].travel_time + possibilities_station_to_destination['walking'].travel_time
        return travel_time