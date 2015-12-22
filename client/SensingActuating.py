#!/usr/bin/python
from sense_hat import SenseHat
from stick import SenseStick
import thread
import config
import Model

# Initialize SenseHat object
sense = None


def keep_sensing(thread_name, s_stick):
    """
    Loop that waits for input, i.e. stick movements that indicate a vehicle movement (enter/leave)
    :param thread_name: name of thread
    :param s_stick: SenseStick object
    """
    print("Starting sensing thread " + thread_name)

    while True:
        # block (with timeout) until an event is available
        s_stick.wait(timeout=10)
        event = s_stick.read()
        key = event.key

        state = Model.get_state()
        print(str(key == config.UP) + "," + str(state))

        if key == config.UP and state == config.RESERVED:
            Model.set_state(config.OCCUPIED)

        if key == config.DOWN and state == config.OCCUPIED:
            Model.leave()

    print("Stopping sensing thread " + thread_name)


def keep_actuating(thread_name, sense_hat):
    """
    Listens for state changes and updates LED colors accordingly.
    :param thread_name: name of thread
    :param sense_hat: SenseHat object
    """
    print("Starting actuating thread " + thread_name)
    old_state = None

    while True:
        # This part of the code could be changed by firmware update
        state = Model.get_state()
        if old_state != state:
            color = (0, 255, 0)

            if state == config.FREE:
                color = (0, 255, 0)

            if state == config.RESERVED:
                color = (255, 165, 0)

            if state == config.OCCUPIED:
                color = (255, 0, 0)

            i = 0
            while i < 64:
                sense_hat.set_pixel(i / 8, i % 8, color)
                i += 1

        old_state = state

    print("Stopping actuating thread " + thread_name)


def init():
    """
    Initialize sensing and actuation of the system.
    """
    global sense
    sense = SenseHat()
    sense.clear()
    # FIXME: Id number is hardcoded.
    sense.show_message("ID=4")
    thread.start_new_thread(keep_actuating, ("Thread-2", sense))
    s_stick = SenseStick()
    thread.start_new_thread(keep_sensing, ("Thread-1", s_stick))


def stop():
    """
    Reset the lights and turn off.
    """
    global sense
    print("Turning off...")
    sense.clear()
