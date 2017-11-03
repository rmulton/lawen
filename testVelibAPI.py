from model.Request import Request
from webservice_caller.VelibAPICaller import VelibAPI

request = Request('48.846559','2.344506','48.8462006','2.2763742')
caller = VelibAPI(request)
res = caller.get_time()
print(res)
