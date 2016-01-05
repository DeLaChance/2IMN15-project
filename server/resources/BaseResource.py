from coapthon.resources.resource import Resource
import os
import sqlite3

class BaseResource(Resource):
    def __init__(self, name, coap_server=None, visible=True, observable=True, allow_children=True):
        super(BaseResource, self).__init__(name, coap_server, visible, observable, allow_children)

        # The resource identifier
        self.index = None

    def _execute_SQL(self, query):
        conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+"/../sqlite.db")
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        conn.close()

        return rows

    def _to_JSON(self, rows):
        if len(rows) is 1:
            return self._record_to_JSON(rows[0])
        else:
            json = "[\n"
            for row in rows:
                json += '  ' + self._record_to_JSON(row) + '\n'

            return json + "]"

    def _record_to_JSON(self, row):
        return "{{parkingSpotId: {}, state: {},  price: {}}}".format(row[0], row[1], row[2])