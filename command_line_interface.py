"""main module for the interface"""

import os
from model.Request import Request

if __name__ == "__main__":
    """main procedure"""
    request_from=[0,0]
    request_to=[0,0]
    test=0
    while test==0:
        request_from[0] = input("What is your position ? enter your latitude (DD mode, as a float)")
        request_from[1] = input("What is your position ? enter you longitude (DD mode, as a float)")
        request_to[0] = input("What is your destination ? enter the latitude (DD mode, as a float)")
        request_to[1] = input("What is your destination ? enter the longitude (DD mode, as a float)")

        """
        example of valid address :
        [48.9 ; 2.25]
        """
        
        request = Request(request_from,request_to)
        """ test si la saisie est valide"""
        if request.request_from=="unvalid" or request.request_to=="unvalid" :
            test=0
        else :
            test=1


print(request.request_from,request.request_to)




