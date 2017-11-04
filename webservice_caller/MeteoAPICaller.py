import requests
import json
import time


"""class that takes for instantiation parameters a date (timestamp) and has for attributes rain and temp (in celsius) """
class MeteoApiCaller:

    url = "http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=BhwEEwV7VHZfcgYxAXcGL1A4BzIAdlVyCnYEZwBlVSgAa1IzD28HYQJsB3oBLgcxUXxXNAswUmILYFYuD31WNwZsBGgFblQzXzAGYwEuBi1QfgdmACBVcgpoBGQAZVUoAGFSNg9yB2ACbAd7ATAHMlFkVygLK1JrC21WMQ9rVjUGZwRjBWBUMV8zBnsBLgY3UGoHMQA%2BVTkKPwQxAGRVMwBkUjMPOQdkAm8HewEyBzVRYVc%2BCz1SYgtpVjIPfVYqBhwEEwV7VHZfcgYxAXcGL1A2BzkAaw%3D%3D&_c=5b261508c1209cb51c6a143438ec616d"
    
    def __init__(self,asked_timestamp):
        self.dico=self.get_meteo_data()
        self.t_date=time.localtime(asked_timestamp)
        self.api_date=self.get_closest_date(self.t_date,self.dico)
        self.rain=self.dico[self.api_date]["pluie"]
        self.temp=self.dico[self.api_date]["temperature"]["sol"]-273.15


    """ call the meteo api and return a dict with the meteo data"""
    def get_meteo_data(self):
        text = requests.get(MeteoApiCaller.url)
        dict = json.loads(text.content)
        return(dict)   

    """
        This function returns the closest date with available data in the meteo api data
        str_dateX are the dates to look for in the dict, since there is only one dict of data every three hours
        The return parameter is a formated string
    """
    def get_closest_date(self,t_date,dico):

        str_date=str(t_date[0])+"-"+str(t_date[1]).zfill(2)+"-"+str(t_date[2]).zfill(2)+" "+str(t_date[3]).zfill(2)+":00:00"
        str_date2=str(t_date[0])+"-"+str(t_date[1]).zfill(2)+"-"+str(t_date[2]).zfill(2)+" "+str(t_date[3]+1).zfill(2)+":00:00"
        str_date3=str(t_date[0])+"-"+str(t_date[1]).zfill(2)+"-"+str(t_date[2]).zfill(2)+" "+str(t_date[3]+2).zfill(2)+":00:00"
        str_date4=str(t_date[0])+"-"+str(t_date[1]).zfill(2)+"-"+str(t_date[2]).zfill(2)+" "+str(t_date[3]+3).zfill(2)+":00:00"

        if str_date in dico :
            asked_date=str_date
        elif str_date2 in dico :
            asked_date=str_date2
        elif str_date3 in dico :
            asked_date=str_date3
        elif str_date4 in dico :
            asked_date=str_date4
        else :
            asked_date="no data available for the time you asked"
            print(asked_date)
        return(asked_date)
