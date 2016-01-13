import sqlite3
import sys
import os
import RequestUtils

DATABASE = os.path.dirname(os.path.realpath(__file__))+"/sqlite.db"

def startReservation(parkingSpotId):
    print("reserveParkingSpot: start")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE parkingspots SET state = 'reserved' WHERE parkingSpotId = {}".format(parkingSpotId))

    connection.commit()
    connection.close()

    # update parkingspot through lwm2m
    endpoint = RequestUtils.findEndpointById(parkingSpotId)
    print("endpoint=" + endpoint)
    RequestUtils.makeReservation(endpoint,"XD-LOL")

def removeReservation(parkingSpotId):
    print("reserveParkingSpot: remove")
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE parkingspots SET state = 'free' WHERE parkingSpotId = {}".format(parkingSpotId))

    connection.commit()
    connection.close()

    # update parkingspot through lwm2m
    endpoint = RequestUtils.findEndpointById(parkingSpotId)
    print("endpoint=" + endpoint)
    RequestUtils.endReservation(endpoint)

def action(action, parkingSpot):
    print("reserveParkingSpot: action=" + str(action) + ",b=" + str(action=="start") + ", parkingSpot=" + str(parkingSpot))
    if action == "start":
        startReservation(parkingSpot)
    if action =="remove":
        removeReservation(parkingSpot)

action(sys.argv[1], sys.argv[2])
