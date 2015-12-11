import config;
import threading;

state = config.FREE;
pID = 4;
reservation = None;
lock = threading.Lock();

def setState(newState):
    global state;
    global lock;

    lock.acquire();

    if( newState < 0 or newState > 2 ):
        print("invalid state: ", newState);
        return;

    state = newState;
    lock.release();

def getState():
    global state;
    global lock;
    lock.acquire();
    s = state;
    lock.release();
    return s;

def getID():
    global pID;
    global lock;
    lock.acquire();
    i=pID;
    lock.release();

    return i;

def getReservation():
    global reservation;
    global lock;
    lock.acquire();
    r=rervation;
    lock.release();

    return r;


def makeReservation(time, licenseplatenumber):
    global reservation;
    global state;
    global lock;
    
    lock.acquire();
    if( reservation != None ):
        print("already reserved");
        lock.release();
        return 1;

    reservation = (time, licenseplatenumber);
    state = config.RESERVED;
    lock.release();   

    return 0;

def leave():
    global reservation;
    global state;
    global lock;

    lock.acquire();
    state = config.FREE;
    reservation = None;
    lock.release();

