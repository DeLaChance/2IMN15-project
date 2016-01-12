import urllib
import httplib
import json
import time
import requests

import sqlite3
import os

def executeSQL(query):
    conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+"/sqlite.db")
    cur = conn.cursor()
    cur.execute(query)

    rows = cur.fetchall()
    conn.commit()
    conn.close()

    return rows

def getState(endpoint):
    query = "SELECT state FROM parkingspots WHERE parkingSpotId='" + endpoint + "'"
    rows = executeSQL(query)

    if( len(rows) == 0 or len(rows) > 1 ):
        print("getState: endpoint=" + endpoint + " not in DB or has copies ?")

    s = str(rows[0][0])
    return s

def makeHTTPRequest(url, method, params):
    r = None
    SERVER_URL = "http://localhost:8080"
    url = SERVER_URL + url
    headers = {"Accept": "application/json, text/plain, */*", "Content-type": "application/json; charset=UTF-8"};

    if( method == "GET"):
        r = requests.get(url, headers = headers)
    if( method == "PUT"):
        r = requests.put(url, data = json.dumps(params), headers = headers)
    if( method == "POST" ):
        r = requests.post(url, data = json.dumps(params), headers = headers)

    return r

def createParkingSpot(ip):
    print("RequestUtils: Creating parking spot with ip=" + ip)

    # gets endpoint belonging to parking spot, can take some time
    i = 0;
    endpoint = None

    while( endpoint == None and i < 10 ):
        i += 1
        time.sleep(i);
        endpoint = resolveEndpoint(ip);
        print("Attempt " + str(i) + " resolving endpoint for ip=" + ip)

    if( i == 10 ):
        print("RequestUtils: resolving endpoint failed, no entry was made")
        return

    pId = resolveId(ip)
    print("RequestUtils: ip=" + ip + ",ParkingSpot: endpoint=" + endpoint)

    # write ParkingSpot to sqliteDB
    if( writeToDB(endpoint, pId) == False ):
        print("RequestUtils: writing endpoint=" + endpoint + " to DB failed, entry already exists or error")

    # observing joystick
    makeHTTPRequest("/api/clients/" + endpoint + "/3345/0/observe","POST",{})


def resolveEndpoint(ip):
    # finds endpoint belonging to ip
    jsondata = makeHTTPRequest("/api/clients","GET",{}).text
    arr = json.loads(jsondata)

    for elem in arr:
        if 'address' in elem and 'endpoint' in elem:
            addr = str( elem['address'] )
            endpoint = str( elem['endpoint'] )

            if ip in addr:
                return endpoint

    return None

def resolveId(ip):
    # finds endpoint belonging to ip
    jsondata = makeHTTPRequest("/api/clients","GET",{}).text
    arr = json.loads(jsondata)
    id = 0;

    return id


def writeToDB(endpoint, pId):
    # creates new entry in sqlite DB
    query = "SELECT * FROM `parkingspots` WHERE parkingSpotId='" + endpoint + "'"
    rows = executeSQL(query)

    if( len(rows) == 0 ):
        # endpoint is a new entry in DB
        insertQuery = "INSERT INTO `parkingspots`(`parkingSpotId`,`state`,`price`, `id`) VALUES ('" + endpoint +"','free',5, '" + str(pId) + "');"
        print("RequestUtils: inserting endpoint=" + endpoint + " into sqliteDB")
        executeSQL(insertQuery)
        return True

    return False

def makeReservation(endpoint, vehicleID):
    # update vehicleID
    makeHTTPRequest("/api/clients/" + endpoint + "/32700/0/32802","PUT",{"id": 32802, "value": vehicleID})
    # update state
    makeHTTPRequest("/api/clients/" + endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "reserved"})
    # update led-display
    makeHTTPRequest("/api/clients/" + endpoint + "/3341/0/5527","PUT",{"id": 5527, "value": "orange"})

def endReservation(endpoint):
    leaveVehicle(endpoint)

def enterOrLeaveVehicle(endpoint):
    s = getState(endpoint)
    if( s == "reserved "):
        enterVehicle(endpoint)
    if( s == "occupied" ):
        leaveVehicle(endpoint)

def enterVehicle(endpoint):
    # update state
    makeHTTPRequest("/api/clients/" + endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "occupied"})
    # update led-display
    makeHTTPRequest("/api/clients/" + endpoint + "/3341/0/5527","PUT",{"id": 5527, "value": "red"})

def leaveVehicle(endpoint):
    # update vehicleID
    makeHTTPRequest("/api/clients/" + endpoint + "/32700/0/32802","PUT",{"id": 32802, "value": ""})
    # update state
    makeHTTPRequest("/api/clients/" + endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "free"})
    # update led-display
    makeHTTPRequest("/api/clients/" + endpoint + "/3341/0/5527","PUT",{"id": 5527, "value": "green"})

