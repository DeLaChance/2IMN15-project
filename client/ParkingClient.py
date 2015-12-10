#!/usr/bin/python
import SensingActuating as sanda;
import time;

def main():
    try:
        sanda.init();
    	while True:
	    	time.sleep(1);

    finally:
        stop();

    stop();

def stop():
    sanda.stop();

if __name__ == "__main__": 
    main();
