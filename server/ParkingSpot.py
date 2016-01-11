import urllib
import httplib
import json
import time
import requests

def makeHTTPRequest(url, method, params, headers):
    r = None

    if( method == "GET"):
        r = requests.get(url, headers = headers)
    if( method == "PUT"):
        r = requests.put(url, data = json.dumps(params), headers = headers)

    return r

class ParkingSpot:

    def __init__(self, ip):
        print("Creating parking spot with ip=" + ip)
        self.ip = ip
        self.SERVER_URL = "http://localhost:8080"
        self.h = {"Accept": "application/json, text/plain, */*", "Content-type": "application/json; charset=UTF-8"};

        while( self.resolveEndpoint() == False ):
            print("Resolving endpoint for ip=" + ip)
            time.sleep(2);
        print("ip=" + self.ip + ",endpoint=" + self.endpoint)

        # test
        """
        time.sleep(2)
        self.makeReservation("XD")
        time.sleep(10)
        self.enterVehicle()
        time.sleep(10)
        self.leaveVehicle()
        """


    def resolveEndpoint(self):
        jsondata = makeHTTPRequest(self.SERVER_URL + "/api/clients","GET",{}, self.h).text
        arr = json.loads(jsondata)

        for elem in arr:
            if 'address' in elem and 'endpoint' in elem:
                addr = str( elem['address'] )
                endpoint = str( elem['endpoint'] )

                if self.ip in addr:
                    self.endpoint = endpoint
                    return True

        return False

    def makeReservation(self, vehicleID):
        # update vehicleID
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/32700/0/32802","PUT",{"id": 32802, "value": vehicleID}, self.h)
        # update state
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "reserved"}, self.h)
        # update led-display
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/3341/0/5527","PUT",{"id": 5527, "value": "orange"}, self.h)

    def enterVehicle(self):
        # update state
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "occupied"}, self.h)
        # update led-display
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/3341/0/5527","PUT",{"id": 5527, "value": "red"}, self.h)

    def leaveVehicle(self):
        # update vehicleID
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/32700/0/32802","PUT",{"id": 32802, "value": ""}, self.h)
        # update state
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "free"}, self.h)
        # update led-display
        makeHTTPRequest(self.SERVER_URL + "/api/clients/" + self.endpoint + "/3341/0/5527","PUT",{"id": 5527, "value": "green"}, self.h)

    def getIP(self):
        return self.ip