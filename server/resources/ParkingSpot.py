from BaseResource import BaseResource

class ParkingSpot(BaseResource):
    def __init__(self, name="ParkingSpot", coap_server=None):
        super(ParkingSpot, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)

    # Method that updates all parking spot states by looking at all reservations
    def _update_parking_spots(self, parkingSpotId):
        query = "UPDATE parkingspots SET state = 'reserved' WHERE parkingSpotId IN (SELECT p.parkingSpotid FROM reservations as r INNER JOIN parkingspots as p ON r.parkingSpotId = p.parkingSpotId WHERE r.'from' < strftime('%s', 'now') AND r.'to' > strftime('%s', 'now') AND p.state = 'free')"

        # Execute SQL
        rows = self._execute_SQL(query)

    def render_GET(self, request):
        # Ensure all parkingspot states are correct
        self._update_parking_spots(self.index)

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
            self.payload = "[]"
        else:
            self.payload = self._to_JSON(rows, self.index is not None)

        return self

    def render_PUT(self, request):
        self.payload = request.payload
        return self

    def render_POST(self, request):
        print "PARKINGSPOT payload: " + request.payload
        return self

    def render_DELETE(self, request):
        return True