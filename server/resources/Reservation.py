from BaseResource import BaseResource

class Reservation(BaseResource):
    def __init__(self, name="Reservation", coap_server=None):
        super(Reservation, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)

    def render_GET(self, request):
        # SQL query to retrieve parking spots
        query = "SELECT * FROM reservations"
        if self.index is not None:
            query += " AND reservationId = {}".format(self.index)

        # Execute SQL
        rows = self._execute_SQL(query)
        print rows

        # Convert to JSON
        self.payload = self._to_JSON(rows)

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