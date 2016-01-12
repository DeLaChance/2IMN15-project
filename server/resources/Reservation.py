import json
import time
import os
from BaseResource import BaseResource
import subprocess
import datetime


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

    # NOT implemented yet!
    # def render_PUT(self, request):
    #     return self

    def render_POST(self, request):
        parkingSpotId = request.options[1].value

        if self.index is not None:
            self.payload = '{"error": true, "message": "No index should be given when using POST"}'
        else:
            data = json.loads(request.payload)
            if data["from"] > data["to"]:
                self.payload = '{"error": true, "message": "The TO value should not be lower than the FROM value}'
            else:
                if not self._fromto_is_ok(parkingSpotId, data["from"], data["to"]):
                    self.payload = '{"error": true, "message": "There already is a reservation on this spot during this time interval"}'
                else:
                    query = "INSERT INTO reservations (vehicleId, parkingSpotId, 'from', 'to') values "
                    query += "({}".format(data["vehicleId"])
                    query += ", {}".format(parkingSpotId)
                    query += ", {}".format(data["from"])
                    query += ", {}".format(data["to"])
                    query += ")"
                    self.payload = self._execute_SQL(query)
                    self.schedule_script("start", parkingSpotId, data["from"])
        return self

    def schedule_script(self, action, id, time):
        """
        Calls the shell script to schedule task at time :time
        Usage example: schedule_script("remove", "2", int(time.time()))
        """

        # format to [[CC]YY]MMDDhhmm[.ss]
        formattedTime = datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%Y%m%d%H%M.%S')

        # call process, make sure the script is executable (chmod +x)
        print("Calling schedule_script action=" + str(action) + ",id=" + str(id) + ",formattedTime=" + str(formattedTime))
        subprocess.call([os.path.dirname(os.path.realpath(__file__))+"/../schedule_script.sh", str(action), str(id), str(formattedTime)])

    def _fromto_is_ok(self, parkingspotId, fromm, to):
        query = "SELECT * FROM reservations WHERE parkingSpotId = {}".format(parkingspotId)
        rows = self._execute_SQL(query)
        if len(rows) != 0:
            for row in rows:
                if fromm <= row["to"] and row["from"] <= to:
                    return False
        return True

    # The following function is called when a vehicle leaves a parking spot.
    # As soon as this happens, the "to" of the reservation has to be changed to the current time,
    # the state has to change from occupied to free,
    # and a bill has to be sent for the vehicleId.
    def render_DELETE(self, request):
        parkingSpotId = request.options[1].value
        free = "free"
        query1 = "SELECT * FROM reservations WHERE reservationId = {}".format(self.index)
        query1 += " AND parkingSpotId = {}".format(parkingSpotId)
        rows = self._execute_SQL(query1)
        query2 = ""
        if len(rows) != 0:
            for row in rows:
                fromm = row["from"]
                to = row["to"]
                current_time = time.time()
                print current_time
                if fromm < current_time < to:

                    query2 += "UPDATE parkingspots SET state = '{}".format(free)
                    query2 += "' WHERE parkingSpotId = {}".format(parkingSpotId)
                    query2 += ";"
                    print self._execute_SQL(query2)

                    query3 = "UPDATE reservations SET 'to'= {} " \
                             "WHERE reservationId = {} " \
                             "AND parkingSpotId = {}".format(current_time, self.index, parkingSpotId)
                    print self._execute_SQL(query3)
                    query4 = "SELECT price FROM parkingspots " \
                             "WHERE parkingSpotId = {}".format(parkingSpotId)
                    rows = self._execute_SQL(query4)
                    price = 0
                    if len(rows) != 0:
                        for row in rows:
                            price = row["price"]
                    duration = current_time - fromm
                    totalCost = duration * price
                    self.payload = '{"price": ' + str(price) + ', "duration": ' + str(duration) + ', "totalcost":' + str(totalCost) + '}'
                else:
                    query5 = "DELETE FROM reservations WHERE reservationId = {} " \
                             "AND parkingSpotId = {}".format(self.index, parkingSpotId)
                    print self._execute_SQL(query5)
                    # delete the reservation

        return self
