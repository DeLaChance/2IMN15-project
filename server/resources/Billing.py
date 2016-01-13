from BaseResource import BaseResource
import time

class Billing(BaseResource):
    def __init__(self, name="Billing", coap_server=None):
        super(Billing, self).__init__(name, coap_server, visible=True,
                                          observable=True, allow_children=True)

    # Method that updates all billing totalCost by looking at all reservations
    def _update_billing(self, vehicleId):
        query1 = "SELECT * FROM reservations WHERE vehicleId = {}".format(vehicleId)
        rows = self._execute_SQL(query1)
        if len(rows) != 0:
            for row in rows:
                reservationId = row["reservationId"]
                parkingSpotId = row["parkingSpotId"]
                fromm = row["from"]
                to = row["to"]
                current_time = time.time()
                duration = 0
                if fromm < current_time:
                    if current_time < to:
                        duration = current_time - fromm
                    else:
                        duration = to - fromm
                query2 = "SELECT * FROM parkingspots WHERE parkingSpotId = {}".format(parkingSpotId)
                rows2 = self._execute_SQL(query2)
                if len(rows2) != 0:
                    for row2 in rows2:
                        price = row2["price"]
                        totalcost = duration * price
                        query3 = "SELECT * FROM billing WHERE reservationId = {}".format(reservationId)
                        rows3 = self._execute_SQL(query3)
                        if len(rows3) != 0:
                            for row3 in rows3:
                                query4 = "UPDATE billing SET totalCost = {} WHERE billingId = {}".format(totalcost, row3["billingId"])
                                print self._execute_SQL(query4)
                        else:
                            query5 = "INSERT INTO billing (reservationId, totalCost) VALUES ({}, {})".format(reservationId, totalcost)
                            print self._execute_SQL(query5)

    def render_GET(self, request):
        # Ensure all parkingspot states are correct
        self._update_billing(self.index)
        # SQL query to retrieve parking spots
        query1 = "SELECT reservationId FROM reservations WHERE vehicleId = {}".format(self.index)
        rows = self._execute_SQL(query1)
        if len(rows) != 0:
            for row in rows:
                query2 = "SELECT * FROM billing WHERE reservationId = {}".format(reservationId)
                rows2 = self._execute_SQL(query2)
                if len(rows2) == 0:
                    self.payload = "[]"
                else:
                    self.payload = self._to_JSON(rows, self.index is not None)
        return self