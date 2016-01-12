#!/usr/bin/env python
from unicurses import *
import time
from termios import tcflush, TCIOFLUSH
from server.coap.CustomClient import CustomClient
import logging
import json

vehicleId = 1

#disable all logging
for name, logger in logging.Logger.manager.loggerDict.iteritems():
    logger.disabled = True

client = None

def chooseParkingSpot():
    print "Enter from and to what time you wish to reserve a spot (MM-DD HH:mm:ss):"
    try:
        fromm = int(time.mktime(time.strptime("2015-"+raw_input("From: "), "%Y-%m-%d %H:%M:%S")))
        to = int(time.mktime(time.strptime("2015-"+raw_input("To:   "), "%Y-%m-%d %H:%M:%S")))
    except:
        print "ERROR: Date was of the wrong format"
        client.stop()
        sys.exit(2)

    spots = json.loads(client.get("/parkingspots", '{{"from": {}, "to": {}}}'.format(fromm, to)).payload)
    choice = printMenu(map((lambda x : "Parking spot " + str(x["parkingSpotId"])), spots))
    print "Parking spot: " + choice

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

    def report_choice(mouse_x, mouse_y):
        i = startx + 2
        j = starty + 3
        for choice in range(0, n_choices):
            if (mouse_y == j + choice) and (mouse_x >= i) and (mouse_x <= i + len(choices[choice])):
                if choice == n_choices - 1:
                    return -1
                else:
                    return choice + 1
                break

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
    mouseinterval(0)
    mousemask(ALL_MOUSE_EVENTS)

    while True:
        c = wgetch(menu_win)
        if c == KEY_UP:
            if highlight == 1:
                highlight == 1
            else:
                highlight -= 1
        elif c == KEY_DOWN:
            if highlight == n_choices:
                highlight = n_choices
            else:
                highlight += 1
        elif c == 10:   # ENTER is pressed
            choice = highlight
            break
        elif c == KEY_MOUSE:
            id, x, y, z, bstate = getmouse()
            if bstate & BUTTON1_PRESSED:
                chosen = report_choice(x + 1, y + 1)
                if chosen != None:
                    highlight = chosen
                    choice = highlight
                    print_menu(menu_win, highlight)
                    time.sleep(0.5)
                    break
                clrtoeol()
                refresh()
                if (chosen == -1):
                    refresh()
                    endwin()
                    client.stop()
                    sys.exit(2)
                print_menu(menu_win, chosen)

        print_menu(menu_win, highlight)

    # flush stdin and out, because mouse event leaks into it
    sys.stdout.flush()
    tcflush(sys.stdin, TCIOFLUSH)
    refresh()
    endwin()

    if choice == len(choices):
        client.stop()
        sys.exit(2)

    return choices[choice-1].replace("Parking spot ", "")

def main():  # pragma: no cover
    global client
    client = CustomClient(server=("127.0.0.1", 5683))

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
