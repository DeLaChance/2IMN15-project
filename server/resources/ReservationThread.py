import sqlite3
import sys
import os
import thread
import time
import RequestUtils

DATABASE = os.path.dirname(os.path.realpath(__file__))+"/../sqlite.db"

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

def action(actionString, parkingSpot, timestamp):
    duration = timestamp - time.time()

    if duration < 0:
        duration = 0

    time.sleep(duration)

    #print("reserveParkingSpot: action=" + str(actionString) + ",b=" + str(actionString=="start") + ", parkingSpot=" + str(parkingSpot))
    if actionString == "start":
        startReservation(parkingSpot)
    if actionString =="remove":
        removeReservation(parkingSpot)

#action(sys.argv[1], sys.argv[2])

def init(actionString, parkingSpotId, time):
    thread.start_new_thread(action, (actionString, parkingSpotId, time))