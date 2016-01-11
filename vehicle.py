#!/usr/bin/env python
from Queue import Queue
import getopt
import random
import sys
from unicurses import *
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

vehicleId = 1

#disable all logging
for name, logger in logging.Logger.manager.loggerDict.iteritems():
    logger.disabled = True

client = None

def chooseParkingSpot():
    #ASK FOR FROM AND TO TIME!!!
    fromm = 1234
    to = 1235

    spots = json.loads(client.get("/parkingspots").payload)
    choice = printMenu(map((lambda x : "Parking spot " + str(x["parkingSpotId"])), spots))
    print choice

    # POST reservation, kijk of het gelukt is
    response = client.post(
        "/parkingspots/"+choice+"/reservations",
        '{{"vehicleId": {}, "from": {}, "to": {}}}'.format(vehicleId, fromm, to)
    )
    print response.payload

    client.stop()
    sys.exit(0)

def printMenu(choices):
    choices.append("Exit")
    n_choices = len(choices)

    WIDTH = 30
    HEIGHT = n_choices+4
    startx = 0
    starty = 0

    highlight = 1
    choice = 0
    c = 0

    def print_menu(menu_win, highlight):
        x = 2
        y = 2
        box(menu_win, 0, 0)
        for i in range(0, n_choices):
            if (highlight == i + 1):
                wattron(menu_win, A_REVERSE)
                mvwaddstr(menu_win, y, x, choices[i])
                wattroff(menu_win, A_REVERSE)
            else:
                mvwaddstr(menu_win, y, x, choices[i])
            y += 1
        wrefresh(menu_win)

    stdscr = initscr()
    clear()
    noecho()
    cbreak()
    curs_set(0)
    startx = int((80 - WIDTH) / 2)
    starty = int((24 - HEIGHT) / 2)

    menu_win = newwin(HEIGHT, WIDTH, starty, startx)
    keypad(menu_win, True)
    mvaddstr(0, 0, "Use arrow keys to go up and down, press ENTER to select a choice")
    refresh()
    print_menu(menu_win, highlight)

    while True:
        c = wgetch(menu_win)
        if c == KEY_UP:
            if highlight == 1:
                highlight == n_choices
            else:
                highlight -= 1
        elif c == KEY_DOWN:
            if highlight == n_choices:
                highlight = 1
            else:
                highlight += 1
        elif c == 10:   # ENTER is pressed
            choice = highlight
            break

        print_menu(menu_win, highlight)
        if choice == 5:
            break

    refresh()
    endwin()

    if choice == len(choices):
        client.stop()
        sys.exit(2)

    return choices[choice-1].replace("Parking spot ", "")

def main():  # pragma: no cover
    global client
    client = HelperClient(server=("127.0.0.1", 5683))

    try:
        chooseParkingSpot()
    except KeyboardInterrupt:
        refresh()
        endwin()
        client.stop()
        sys.exit(2)

    # response = client.post(path, payload)
    #
    # response = client.delete(path)
    client.stop()
    sys.exit(2)

if __name__ == '__main__':  # pragma: no cover
    main()
