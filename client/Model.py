import config
import threading

# Initiate the state to free
state = config.FREE

# Set pID identical to our group number
# FIXME: Put this in config.py?
pID = 4

# Initiate reservation to None
# FIXME: Depending on protocol we can have multiple reservations, but none that overlap.
reservation = None

# Thread lock
lock = threading.Lock()


def set_state(new_state):
    """
    Saves a state to the model
    :param new_state: the state to save
    :return: whether state is saved
    """
    global state
    global lock

    lock.acquire()

    if new_state < 0 or new_state > 2:
        print("invalid state: ", new_state)
        return False

    state = new_state
    lock.release()

    return True


def get_state():
    """
    Get current state
    :return: current state
    """
    global state
    global lock
    lock.acquire()
    s = state
    lock.release()
    return s


def get_id():
    """
    Get process id
    :return: process id
    """
    global pID
    global lock
    lock.acquire()
    i = pID
    lock.release()

    return i


def get_reservation():
    """
    Get saved reservation
    :return: reservation
    """
    global reservation
    global lock
    lock.acquire()
    r = reservation
    lock.release()

    return r


def make_reservation(start_time, time, license_plate_number):
    """
    Make a new reservation
    :param start_time: start time of reservation
    :param time: length of reservation
    :param license_plate_number: vehicle id
    :return: whether the reservation was successful
    """
    global reservation
    global state
    global lock
    
    lock.acquire()
    if reservation is not None:
        print("already reserved")
        lock.release()
        return True

    reservation = (start_time, time, license_plate_number)
    state = config.RESERVED
    lock.release()

    return False


def leave():
    """
    Vehicle leaves Parking Spot
    """
    global reservation
    global state
    global lock

    lock.acquire()
    state = config.FREE
    reservation = None
    lock.release()
