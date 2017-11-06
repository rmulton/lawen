from webservice_caller._ParisOpenDataAPICaller import _ParisOpenDataAPICaller
from model.Transport.Velib import Velib

class VelibAPICaller(_ParisOpenDataAPICaller):
    
    def __init__(self,request):
        super().__init__(request)
        self._url = self._url.format('?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=bonus&facet=status&facet=contract_name')
        self._modes = {'bicycling':Velib}