from BaseResource import BaseResource
import json

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

        payload = json.loads(request.payload)
        fromm = payload["from"]
        to = payload["to"]

        # SQL query to retrieve parking spots
        if self.index is not None:
            query = "SELECT parkingSpotId, state, price FROM parkingspots as p"
            query += " WHERE p.parkingSpotId = {}".format(self.index)
        else:
            query = "SELECT parkingSpotId, 'free' as state, price FROM parkingspots "
            query += " WHERE parkingSpotId NOT IN"
            query += " (SELECT p.parkingSpotId FROM parkingspots as p"
            query += " INNER JOIN reservations as r"
            query += " ON r.parkingSpotId = p.parkingSpotId"
            query += " WHERE  r.'from' < {}".format(to)
            query += " OR r.'to' > {})".format(fromm)

        # Execute SQL
        rows = self._execute_SQL(query)

        # Convert to JSON
        if len(rows) == 0:
            self.payload = "[]"
        else:
            self.payload = self._to_JSON(rows, self.index is not None)

        return self