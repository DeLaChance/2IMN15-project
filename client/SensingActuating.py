#!/usr/bin/python
from sense_hat import SenseHat
from Stick import SenseStick
import thread
import config
import time
import os
import socket

# Initialize SenseHat object
sense = SenseHat()

def getState():
    import os.path
    lockfileuri = config.HOME_DIR + "displaylock.txt"
    displayfileuri = config.HOME_DIR + "displaylock.txt"

    while( os.path.exists(lockfileuri) ):
        time.sleep(1);

    # open lock file and display file
    f1 = open(lockfileuri, 'w')
    f2 = open(displayfileuri, 'r+')

    s = f2.read();

    # delete lock file
    os.remove(lockfileuri)

    return s

def setState(s):
    import os.path
    lockfileuri = config.HOME_DIR + "displaylock.txt"
    displayfileuri = config.HOME_DIR + "display.txt"

    while( os.path.exists(lockfileuri) ):
        time.sleep(1);

    # open lock file and display file
    f1 = open(lockfileuri, 'w')
    f2 = open(displayfileuri, 'w')

    f2.write(s);

    # delete lock file
    os.remove(lockfileuri)

def setJoyStickState(s):
    import os.path
    lockfileuri = config.HOME_DIR + "jslock.txt"
    jsfileuri = config.HOME_DIR + "js.txt"

    while( os.path.exists(lockfileuri) ):
        time.sleep(1);

    # open lock file and display file
    f1 = open(lockfileuri, 'w')
    f2 = open(jsfileuri, 'w')

    f2.write(s)

    # delete lock file
    os.remove(lockfileuri)

def keepSensingJoyStick(thread_name, s_stick):

    i = 0;
    print("Starting joystick thread " + thread_name)

    while True:
        # block (with timeout) until an event is available
        s_stick.wait(timeout=10)
        event = s_stick.read()
        key = event.key

        state = getState()
        if( i > 10000 ):
            print("keepSensingJoyStick: key=" + str(key) + ",state=" + str(state))
            i = 0;
        i += 1;

        if key == config.UP and state == config.RESERVED:
            #enter vehicle
            setState(config.OCCUPIED)
            setJoyStickState(config.UP)

        if key == config.DOWN and state == config.OCCUPIED:
            #leave vehicle
            setState(config.FREE)
            setJoyStickState(config.DOWN)

    print("Stopping joystick thread " + thread_name)


def keepUpdatingDisplay(thread_name, sense):
    old_state = None
    print("Starting display thread " + thread_name)

    while True:
        state = getState()
        if old_state != state:
            print("keepUpdatingDisplay: state=" + state)
            color = (0, 255, 0)

            if state == config.FREE:
                color = (0, 255, 0)

            if state == config.RESERVED:
                color = (255, 165, 0)

            if state == config.OCCUPIED:
                color = (255, 0, 0)

            i = 0
            while i < 64:
                sense.set_pixel(i / 8, i % 8, color)
                i += 1

        old_state = state

    print("Stopping display thread " + thread_name)

def main():
    global sense
    sense = SenseHat()
    sense.clear()
    s_stick = SenseStick()

    # start two threads that actually update the display and listen to the joystick
    thread.start_new_thread(keepUpdatingDisplay, ("keepUpdatingDisplayThread", sense))
    #thread.start_new_thread(keepSensingJoyStick, ("keepSensingJoyStickThread", s_stick))

    # listen for server ip inbound on port 4000
    print("start looking up serverip")
    # assumes that avahi-publish has been started already
    s = socket.socket() # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 4000 # Reserve a port for your service.

    s.bind((host, port))
    s.listen(5);
    (c,addr) = s.accept()
    serverip = str( c.recv(1024) ) # contains server ip
    print("serverip=" + serverip)
    s.close()

    f = open(config.HOME_DIR + "serverip.txt", 'w')
    f.write(serverip)
    f.close()

    keepSensingJoyStick("keepSensingJoyStickThread", s_stick) # might as well run this in the main thread


if __name__ == '__main__':
    main()