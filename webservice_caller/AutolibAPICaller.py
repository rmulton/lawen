from webservice_caller.ParisOpenDataAPI import _SharedAPICaller

class AutolibAPI(_SharedAPICaller):
    
    def __init__(self,request):
        super().__init__(request)
        self.url = self.url.format('?dataset=autolib-disponibilite-temps-reel&facet=charging_status&facet=kind&facet=postal_code&facet=slots&facet=status&facet=subscription_status')
        self.mode = "driving"