from BaseResource import BaseResource

class Reservation(BaseResource):
    def __init__(self, name="Reservation", coap_server=None):
        super(Reservation, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)

    def render_GET(self, request):
        parkingSpotId = request.options[1].value

        # SQL query to retrieve reservations
        query = "SELECT * FROM reservations"
        if self.index is not None:
            query += " WHERE reservationId = {}".format(self.index)

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
        res = Reservation()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True