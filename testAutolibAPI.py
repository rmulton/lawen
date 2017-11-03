from model.Request import Request
from webservice_caller.AutolibAPICaller import AutolibAPI

request = Request('48.846559','2.344506','48.8462006','2.2763742')
caller = AutolibAPI(request)
res = caller.get_time()
print(res)
