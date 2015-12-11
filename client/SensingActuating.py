#!/usr/bin/python
from sense_hat import SenseHat
import stick
from stick import SenseStick

import thread
import time

import config
import Model

def keepSensing(threadName,sstick):
    print("Starting sensing thread " + threadName);

    while True:
        sstick.wait(timeout=10); # block (with timeout) until an event is available 
        event = sstick.read();
        key = event.key;

        state = Model.getState();
        print(str(key == config.UP) + "," + str(state));

        if( key == config.UP and state == config.RESERVED ):
            Model.setState(config.OCCUPIED);

        if( key == config.DOWN and state == config.OCCUPIED ):
            Model.leave();

    print("Stopping sensing thread " + threadName);

def keepActuating(threadName,sense):
    print("Starting actuating thread " + threadName);
    oldState = None;

    while True:
        # This part of the code could be changed by firmware update
        state = Model.getState();
        if( oldState != state ):
            color = (0,255,0);

            if( state == config.FREE ):
                color = (0,255,0);

            if( state == config.RESERVED ):
                color = (255, 165, 0);

            if( state == config.OCCUPIED ):
                color = (255, 0, 0);

            i = 0;
            while(i < 64):
                sense.set_pixel(i / 8, i % 8, color );
                i += 1;

        oldState = state;

    print("Stopping actuating thread " + threadName);

def init():
    sense = SenseHat();
    sense.clear();
    sense.show_message("ID=4");
    thread.start_new_thread( keepActuating, ("Thread-2",sense));


    sstick = SenseStick();
    thread.start_new_thread( keepSensing, ("Thread-1",sstick));

def stop():
    global sense;
    print("Turning off...");
    sense.clear();
