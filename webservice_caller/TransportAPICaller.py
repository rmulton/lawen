import abc
from model.Possibilities import Possibilities

class TransportAPICaller:
    '''
    Class that all api callers that handle computing itiniraries inherit from
    '''
    __metaclass__ = abc.ABCMeta

    def __init__():
        self.modes = {}
    
    @abc.abstractmethod
    def get_time(self):
        return
    
    @abc.abstractmethod
    def get_itinerary(self):
        return

    def get_possibilities(self):  
        '''
        returns a list of transportation objects containing each its time and itinerary 
        ''' 
        travel_time = self.get_times()
        itinerary = self.get_itineraries()
        transports = {}
        for transport_name, transport_class in self.modes.items():
            new_transport = transport_class(travel_time[transport_name], itinerary[transport_name])
            transports[transport_name] = new_transport
        return Possibilities(transports)