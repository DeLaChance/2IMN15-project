from coapthon.resources.resource import Resource

class ParkingSpot(Resource):
    def __init__(self, name="ParkingSpot", coap_server=None):
        super(ParkingSpot, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "Parking spot"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.payload = request.payload
        return self

    def render_POST(self, request):
        res = ParkingSpot()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True