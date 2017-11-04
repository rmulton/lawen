from webservice_caller.ParisOpenDataAPI import _SharedAPICaller
from model.Transport.Velib import Velib

class VelibAPI(_SharedAPICaller):
    
    def __init__(self,request):
        super().__init__(request)
        self.url = self.url.format('?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=bonus&facet=status&facet=contract_name')
        self.mode = {'bicycling':Velib}