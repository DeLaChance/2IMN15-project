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

serverip = ""

def getState():
    import os.path
    lockfileuri = config.HOME_DIR + "displaylock.txt"
    displayfileuri = config.HOME_DIR + "display.txt"

    while( os.path.exists(lockfileuri) ):
        time.sleep(1);

    # open lock file and display file
    f1 = open(lockfileuri, 'w')
    f2 = open(displayfileuri, 'r+')

    f1.write("a")
    s = f2.read()
    f1.close()
    f2.close()

    # delete lock file
    os.remove(lockfileuri)

    return s

def setState(s):
    import os.path
    lockfileuri = config.HOME_DIR + "displaylock.txt"
    displayfileuri = config.HOME_DIR + "display.txt"

    while( os.path.exists(lockfileuri) ):
        time.sleep(1);

    print("Python: entering critical section display")

    # open lock file and display file
    f1 = open(lockfileuri, 'w')
    f2 = open(displayfileuri, 'w')

    f1.write("a")
    f2.write(s)

    f1.close()
    f2.close()
    # delete lock file
    os.remove(lockfileuri)
    print("Python: leaving critical section display")

def setJoyStickState(s):
    import os.path
    lockfileuri = config.HOME_DIR + "jslock.txt"
    jsfileuri = config.HOME_DIR + "js.txt"

    if( os.path.exists(jsfileuri) ):
        print("Python: jslock.txt exists, no need to push joystick state")
        return

    while( os.path.exists(lockfileuri) ):
        time.sleep(1);

    print("Python: entering critical section joystick")

    # open lock file and display file
    f1 = open(lockfileuri, 'w')
    f2 = open(jsfileuri, 'w')

    f1.write("a")
    f2.write(s)

    f1.close()
    f2.close()

    # delete lock file
    os.remove(lockfileuri)
    print("Python: leaving critical section joystick")

def keepSensingJoyStick(thread_name, s_stick):

    print("Starting joystick thread " + thread_name + "\n")
    oldKey = None

    while True:
        # block (with timeout) until an event is available
        s_stick.wait(timeout=10)
        event = s_stick.read()
        key = event.key

        if( oldKey != key and (key == config.UP or key == config.DOWN) ):
            if key == config.UP:
                #enter vehicle
                print("Python: joystick is up")
                setJoyStickState(str(config.UP))

            if key == config.DOWN:
                #leave vehicle
                print("Python: joystick is down")
                setJoyStickState(str(config.DOWN))

        oldKey = key

    print("Stopping joystick thread " + thread_name + "\n")



def keepUpdatingDisplay(thread_name, sense):
    old_state = None
    color = (0, 255, 0)
    print("Starting display thread " + thread_name + "\n")

    while True:
        state = getState()
        if old_state != state:
            print("keepUpdatingDisplay: state=" + state + "\n")

            if state == "green":
                color = (0, 255, 0)

            if state == "orange":
                color = (255, 165, 0)

            if state == "red":
                color = (255, 0, 0)

            i = 0
            while i < 64:
                sense.set_pixel(i / 8, i % 8, color)
                i += 1

        old_state = state

    print("Stopping display thread " + thread_name + "\n")

def main():
    global sense
    global serverip
    sense = SenseHat()
    sense.clear()
    s_stick = SenseStick()

    # start two threads that actually update the display and listen to the joystick
    thread.start_new_thread(keepUpdatingDisplay, ("keepUpdatingDisplayThread", sense))
    #thread.start_new_thread(keepSensingJoyStick, ("keepSensingJoyStickThread", s_stick))

    # listen for server ip inbound on port 4000
    print("start looking up serverip \n")
    # assumes that avahi-publish has been started already
    s = socket.socket() # Create a socket object
    host = "127.0.0.1" # Get local machine name
    port = 4000 # Reserve a port for your service.

    s.bind((host, port))
    s.listen(5);
    b = True

    while( b ):
        (c,addr) = s.accept()
        data = c.recv(1024)
        if data != None:
            serverip = str( data ) # contains server ip
            b = False

    print("serverip=" + serverip + "\n")
    c.close()
    s.close()

    f = open(config.HOME_DIR + "serverip.txt", 'w')
    f.write(serverip)
    f.close()

    keepSensingJoyStick("keepSensingJoyStickThread", s_stick) # might as well run this in the main thread


if __name__ == '__main__':
    main()