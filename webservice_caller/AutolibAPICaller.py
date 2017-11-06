from webservice_caller._ParisOpenDataAPICaller import _ParisOpenDataAPICaller
from model.Transport.Autolib import Autolib

class AutolibAPICaller(_ParisOpenDataAPICaller):
    
    def __init__(self,request):
        super().__init__(request)
        self.url = self.url.format('?dataset=autolib-disponibilite-temps-reel&facet=charging_status&facet=kind&facet=postal_code&facet=slots&facet=status&facet=subscription_status')
        self.modes =  {'driving':Autolib}