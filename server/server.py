from coap.CustomCoAP import CustomCoAP
from resources.ParkingSpot import ParkingSpot
from resources.Reservation import Reservation

class CoAPServer(CustomCoAP):
    def __init__(self, host, port):
        CustomCoAP.__init__(self, (host, port))
        self.add_resource('parkingspots/', ParkingSpot())
        self.add_resource('parkingspots/*/reservations/', Reservation())

def main():
    server = CoAPServer("127.0.0.1", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."

if __name__ == '__main__':
    main()