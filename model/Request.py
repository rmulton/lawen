class Request():

    def __init__(self,request_from,request_to):
        self._request_from = self.check_request_from(request_from)
        self._request_to = self.check_request_to(request_to)



    """ check methods for _request_from and _request_to attributes """


    def check_request_from(self, request_from):
        try:
            request_from[0] = float(request_from[0])
            request_from[1] = float(request_from[1])
            assert request_from[0] > 48.818343 and request_from[0] < 48.905555 and request_from[1] > 2.240706 and request_from[1] < 2.412400

        except AssertionError:
            print("The origin address you typed is not in Paris")
            return "unvalid"
        except ValueError:
            print("You didn't type a valid origin address (not convertible in float)")
            return "unvalid"
        else :
            return request_from

    def check_request_to(self, request_to):
        try:
            request_to[0] = float(request_to[0])
            request_to[1] = float(request_to[1])
            assert request_to[0] > 48.818343 and request_to[0] < 48.905555 and request_to[1] > 2.240706 and request_to[1] < 2.412400
        except AssertionError:
            print("The destination address you typed is not in Paris")
            return "unvalid"
        except ValueError:
            print("You didn't type a valid destination address (not convertible in float)")
            return "unvalid"
        else :
            return request_to

    """ getters and setters de _request_from et _request_to """

    def _get_request_from(self):
        return self._request_from

    def _set_request_from(self,request_from):
        print("Don't change the f*cking adress, yo")


    request_from=property(_get_request_from,_set_request_from)



    def _get_request_to(self):
        return self._request_to

    def _set_request_to(self,request_to):
        print("Don't change the f*cking adress, yo")

    request_to=property(_get_request_to,_set_request_to)



