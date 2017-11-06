import requests
import json
import time


class WeatherAPICaller:
"""class that takes for instantiation parameters a date (timestamp) and has for attributes rain and temp (in celsius) """

    url = "http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=BhwEEwV7VHZfcgYxAXcGL1A4BzIAdlVyCnYEZwBlVSgAa1IzD28HYQJsB3oBLgcxUXxXNAswUmILYFYuD31WNwZsBGgFblQzXzAGYwEuBi1QfgdmACBVcgpoBGQAZVUoAGFSNg9yB2ACbAd7ATAHMlFkVygLK1JrC21WMQ9rVjUGZwRjBWBUMV8zBnsBLgY3UGoHMQA%2BVTkKPwQxAGRVMwBkUjMPOQdkAm8HewEyBzVRYVc%2BCz1SYgtpVjIPfVYqBhwEEwV7VHZfcgYxAXcGL1A2BzkAaw%3D%3D&_c=5b261508c1209cb51c6a143438ec616d"
    
    def __init__(self,required_timestamp):
        self._weather_data = self.get_meteo_data()
        self._t_date = time.localtime(required_timestamp)
        self._api_date = self.get_closest_date()

    @property
    def rain(self):
        return self._weather_data[self._api_date]["pluie"]

    @property
    def temp(self):
        return self._weather_data[self._api_date]["temperature"]["sol"]-273.15


    def get_meteo_data(self):
    """ call the meteo api and return a dict with the meteo data"""
        text = requests.get(WeatherAPICaller.url)
        weather_data = json.loads(text.content)
        return weather_data

    def get_closest_date(self):
    """
        This function returns the closest date with available data in the meteo api data
        str_dateX are the dates to look for in the dict, since there is only one dict of data every three hours
        The return parameter is a formated string
    """
        str_date=str(self._t_date[0])+"-"+str(self._t_date[1]).zfill(2)+"-"+str(self._t_date[2]).zfill(2)+" "+str(self._t_date[3]).zfill(2)+":00:00"
        str_date2=str(self._t_date[0])+"-"+str(self._t_date[1]).zfill(2)+"-"+str(self._t_date[2]).zfill(2)+" "+str(self._t_date[3]+1).zfill(2)+":00:00"
        str_date3=str(self._t_date[0])+"-"+str(self._t_date[1]).zfill(2)+"-"+str(self._t_date[2]).zfill(2)+" "+str(self._t_date[3]+2).zfill(2)+":00:00"
        str_date4=str(self._t_date[0])+"-"+str(self._t_date[1]).zfill(2)+"-"+str(self._t_date[2]).zfill(2)+" "+str(self._t_date[3]+3).zfill(2)+":00:00"

        if str_date in self._weather_data :
            asked_date=str_date
        elif str_date2 in self._weather_data :
            asked_date=str_date2
        elif str_date3 in self._weather_data :
            asked_date=str_date3
        elif str_date4 in self._weather_data :
            asked_date=str_date4
        else :
            asked_date="no data available for the time you asked"
        return asked_date
