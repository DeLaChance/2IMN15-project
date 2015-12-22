#!/usr/bin/python
import SensingActuating as Sanda
import time
import Model


def main():
    """
    Initializes SensingActuating module and unit tests the model.
    """
    try:
        Sanda.init()
        while True:
            Model.make_reservation(5, 10, 10)
            time.sleep(5)

    finally:
        stop()

    stop()


def stop():
    """
    Stops the SensingActuating module
    """
    Sanda.stop()

# Calls the main function on run
if __name__ == "__main__":
    main()
