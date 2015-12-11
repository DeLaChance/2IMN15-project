#!/usr/bin/python
import SensingActuating as sanda;
import time;
import Model;

def main():
    try:
        sanda.init();
    	while True:
            Model.makeReservation(10,10);
            time.sleep(5);

    finally:
        stop();

    stop();

def stop():
    sanda.stop();

if __name__ == "__main__": 
    main();
