import json
import time
from BaseResource import BaseResource


class Reservation(BaseResource):
    def __init__(self, name="Reservation", coap_server=None):
        super(Reservation, self).__init__(name, coap_server, visible=True,
                                          observable=True, allow_children=True)

    def render_GET(self, request):
        parkingSpotId = request.options[1].value

        # SQL query to retrieve reservations
        query = "SELECT * FROM reservations WHERE parkingSpotId = {}".format(parkingSpotId)
        if self.index is not None:
            query += " AND reservationId = {}".format(self.index)

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
        if self.index is not None:
            self.payload = '{"error": true, "message": "No index should be given when using POST"}'
        else:
            data = json.loads(request.payload)
            if data["from"] > data["to"]:
                self.payload = '{"error": true, "message": "The TO value should not be lower than the FROM value}'
            else:
                if not self._fromto_is_ok(data["parkingSpotId"], data["from"], data["to"]):
                    self.payload = '{"error": true, "message": "There already is a reservation on this spot during this time interval"}'
                else:
                    query = "INSERT INTO reservations (vehicleId, parkingSpotId, 'from', 'to') values "
                    query += "({}".format(data["vehicleId"])
                    query += ", {}".format(data["parkingSpotId"])
                    query += ", {}".format(data["from"])
                    query += ", {}".format(data["to"])
                    query += ")"
                    self.payload = self._execute_SQL(query)
                    print query
        return self

    def _fromto_is_ok(self, parkingspotId, fromm, to):
        query = "SELECT * FROM reservations WHERE parkingSpotId = {}".format(parkingspotId)
        rows = self._execute_SQL(query)
        if len(rows) != 0:
            for row in rows:
                if fromm <= row["to"] and row["from"] <= to:
                    return False
        return True

    def render_DELETE(self, request):
        data = json.loads(request.payload)
        state = "free"
        fromm = data["from"]
        to = data["to"]
        query = "DELETE FROM reservations WHERE reservationId = {}".format(self.index)
        query += " AND parkingSpotId = {}".format(data["parkingSpotId"])
        current_time = time.time()
        if fromm < current_time < to:
            query += "; UPDATE parkingspots SET state = {}".format(state)
            query += " WHERE parkingSpotId = {}".format(data["parkingSpotId"])
            query += ";"
        print self._execute_SQL(query)
        return self
