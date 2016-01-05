from BaseResource import BaseResource

class ParkingSpot(BaseResource):
    def __init__(self, name="ParkingSpot", coap_server=None):
        super(ParkingSpot, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)

    def render_GET(self, request):
        # SQL query to retrieve parking spots
        query = "SELECT * FROM parkingspots"
        if self.index is not None:
            query += " WHERE parkingSpotId = {}".format(self.index)
        else:
            query += " WHERE state = 'free'"

        # Execute SQL
        rows = self._execute_SQL(query)

        # Convert to JSON
        if len(rows) == 0:
            self.payload = None
        else:
            self.payload = self._to_JSON(rows)

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