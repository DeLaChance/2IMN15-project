import config
import threading

# Initiate the state to free
state = config.FREE

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

    if new_state < config.FREE or new_state > config.RESERVED:
        print("invalid state: ", new_state)
        return False

    lock.acquire()
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
