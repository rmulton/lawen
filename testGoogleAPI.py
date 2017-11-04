from model.Request import Request
from webservice_caller.GoogleAPI import GoogleAPICaller

request = Request('48.846559','2.344506','48.8462006','2.2763742')
caller = GoogleAPICaller(request)
res = caller.get_possibilities()
print(res)
