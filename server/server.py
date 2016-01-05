from coapthon.server.coap import CoAP
from resources.ParkingSpot import ParkingSpot
from resources.Reservation import Reservation
from CustomRequestLayer import CustomRequestLayer


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self._requestLayer = CustomRequestLayer(self)  # Override library layer to support RESTful URIs

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