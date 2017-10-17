from model.Request import Request
from webservice_caller.GoogleAPI import GoogleAPICaller

request = Request([48.8809481,2.3568375],[48.7549066,2.3010135])
caller = GoogleAPICaller(request)
caller.get_possibilities()
