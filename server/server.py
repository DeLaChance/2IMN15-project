from coap.CustomCoAP import CustomCoAP
from resources.ParkingSpot import ParkingSpot
from resources.Reservation import Reservation
from resources.BaseResource import BaseResource

import SpotFinderThread
import sys

class CoAPServer(CustomCoAP):
    def __init__(self, host, port):
        CustomCoAP.__init__(self, (host, port))
        self.add_resource('parkingspots/', ParkingSpot())
        self.add_resource('parkingspots/*/reservations/', Reservation())
        self.add_resource('vehicles/', BaseResource("Vehicle"))
        self.add_resource('vehicles/*/reservations/', Reservation())

def main():
    # if( len(sys.argv) < 2 ):
    #     print("usage: python2.7 <own_IP>")
    #     return

    # print("Starting initProcess with serverip=" + sys.argv[1])
    # if( len(sys.argv) == 3 ):
    #     SpotFinderThread.init(sys.argv[1], sys.argv[2])
    # else:
    #     SpotFinderThread.init(sys.argv[1], "")

    server = CoAPServer("127.0.0.1", 5700)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."

if __name__ == '__main__':
    main()