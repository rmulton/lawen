from webservice_caller._ParisOpenDataAPICaller import _ParisOpenDataAPICaller

class VelibAPICaller(_ParisOpenDataAPICaller):
    
    def __init__(self,request):
        super().__init__(request)
        self.url = self.url.format('?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=bonus&facet=status&facet=contract_name')
        self.mode = "bicycling"