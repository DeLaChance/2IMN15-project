from coapthon.resources.resource import Resource
import os
import json
import sqlite3

class BaseResource(Resource):
    def __init__(self, name, coap_server=None, visible=True, observable=True, allow_children=True):
        super(BaseResource, self).__init__(name, coap_server, visible, observable, allow_children)

        # The resource identifier
        self.index = None

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _execute_SQL(self, query):
        conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+"/../sqlite.db")
        conn.row_factory = self._dict_factory
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        conn.close()

        return rows

    def _to_JSON(self, rows):
        # Do not make a single object a 1 element array
        if len(rows) == 1:
            return json.dumps(rows)[1:-1]

        return json.dumps(rows)