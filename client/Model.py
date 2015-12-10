import config;

state = config.FREE;
pID = 4;

def setState(newState):
    global state;
    if( newState < 0 or newState > 2 ):
        print("invalid state: ", newState);
        return;

    state = newState;
    

def getState():
    global state;
    return state;

def getID():
    return ID;

def getReservation():

def makeReservation()
