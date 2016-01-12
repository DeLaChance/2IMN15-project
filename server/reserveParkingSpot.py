import sqlite3
import sys
import RequestUtils

DATABASE = 'sqlite.db'

def startReservation(parkingSpotId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE parkingspots SET state = 'reserved' WHERE parkingSpotId = {}".format(parkingSpotId))

    # update parkingspot through lwm2m
    RequestUtils.makeReservation(parkingSpotId,"XD-LOL")

    connection.commit()
    connection.close()

def removeReservation(parkingSpotId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE parkingspots SET state = 'free' WHERE parkingSpotId = {}".format(parkingSpotId))

    # update parkingspot through lwm2m
    RequestUtils.endReservation(parkingSpotId)

    connection.commit()
    connection.close()

def action(action, parkingSpot):
    if action == "start":
        startReservation(parkingSpot)
    if action =="remove":
        removeReservation(parkingSpot)

action(sys.argv[1], sys.argv[2])
