#!/usr/bin/python
from sense_hat import SenseHat

from pisense import SenseStick

sense = None;

def initSensing():
	sense = SenseHat();
	sense.clear();
	#sense.show_message("Parking spot on!");

	stick = SenseStick()

