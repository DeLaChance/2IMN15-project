#!/usr/bin/env python
from Queue import Queue
import getopt
import random
import sys
import threading
from coapthon import defines
from coapthon.client.coap import CoAP
from coapthon.client.helperclient import HelperClient
from coapthon.messages.message import Message
from coapthon.messages.request import Request
from coapthon.utils import parse_uri
import logging
import json
# from picker import *

#disable all logging
for name, logger in logging.Logger.manager.loggerDict.iteritems():
    logger.disabled = True

client = None

def spotname(parkingspot):
    return "Parking spot " + parkingspot["parkingSpotId"]

def chooseParkingSpot():
    print "The following parking spots are available at the moment: "
    # spots = json.loads(string)
    spots = json.loads(client.get("/parkingspots").payload)
    for spot in spots:
        print "[parking spot] id: " + str(spot["parkingSpotId"]) + ", price: " + str(spot["price"])
    print "Choose your parking spot by typing its Id"
    print "if you want to reload the available parking spots, press r"
    print "if you want to make a reservation for a spot, continue by pressing m"
    # print "if you want to delete a reservation, continue by pressing d"
    print "if you want to view the reservations from one parking spot, continue by pressing v"
    check = True
    while check:
        chosen = raw_input()
        if chosen == "r":
            chooseParkingSpot()
        elif chosen == "m":
            makeReservation()
        elif chosen == "d":
            viewReservations()
        else:
            print "Unrecognized choice."
            continue
        check = False
        break
    client.close()
    sys.exit(2)

def makeReservation():
    print "Choose which parking spot you want to reserve by pressing its id"

def viewReservations():
    print "Choose which parking spot you want to view the reservations from"
    parkingspot = raw_input()
    reservations = json.loads(client.get("/parkingspots/" + parkingspot + "/reservations"))
    print "All reservations:"
    print reservations

def chooseParkingSpot2():
    spots = client.get("/parkingspots").payload
    opts = Picker(
        title = 'Choose your parking spot',
        options = map(spotname, spots)
    ).getSelected()

    if opts == False:
        print "Aborted!"
    else:
        print opts
    # for spot in spots
    # print spot + "/"
    client.close()
    sys.exit(2)

def main():  # pragma: no cover
    global client
    client = HelperClient(server=("127.0.0.1", 5683))
    chooseParkingSpot()

    # response = client.post(path, payload)
    #
    # response = client.delete(path)
    sys.exit(2)

if __name__ == '__main__':  # pragma: no cover
    main()
