from coap.CustomCoAP import CustomCoAP
from resources.ParkingSpot import ParkingSpot
from resources.Reservation import Reservation

import SpotFinderThread
import sys

class CoAPServer(CustomCoAP):
    def __init__(self, host, port):
        CustomCoAP.__init__(self, (host, port))
        self.add_resource('parkingspots/', ParkingSpot())
        self.add_resource('parkingspots/*/reservations/', Reservation())

def main():
    if( len(sys.argv) < 2 ):
        print("usage: python2.7 <own_IP>")

    server = CoAPServer("127.0.0.1", 5683)

    print("Starting initProcess...")
    # SpotFinderThread.init(sys.argv[1])

    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."

if __name__ == '__main__':
    main()