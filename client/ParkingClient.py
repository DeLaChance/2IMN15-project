#!/usr/bin/python
import SensingActuating as Sanda
import time
import Model


def main():
    try:
        Sanda.init()
        while True:
            Model.make_reservation(10, 10)
            time.sleep(5)

    finally:
        stop()

    stop()


def stop():
    Sanda.stop()


if __name__ == "__main__":
    main()
