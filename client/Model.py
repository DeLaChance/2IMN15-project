import config
import threading

state = config.FREE
pID = 4
reservation = None
lock = threading.Lock()


def set_state(new_state):
    global state
    global lock

    lock.acquire()

    if new_state < 0 or new_state > 2:
        print("invalid state: ", new_state)
        return

    state = new_state
    lock.release()


def get_state():
    global state
    global lock
    lock.acquire()
    s = state
    lock.release()
    return s


def get_id():
    global pID
    global lock
    lock.acquire()
    i = pID
    lock.release()

    return i


def get_reservation():
    global reservation
    global lock
    lock.acquire()
    r = reservation
    lock.release()

    return r


def make_reservation(time, license_plate_number):
    global reservation
    global state
    global lock
    
    lock.acquire()
    if reservation is not None:
        print("already reserved")
        lock.release()
        return 1

    reservation = (time, license_plate_number)
    state = config.RESERVED
    lock.release()

    return 0


def leave():
    global reservation
    global state
    global lock

    lock.acquire()
    state = config.FREE
    reservation = None
    lock.release()
