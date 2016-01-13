import json, time, sqlite3
from flask import Flask, render_template
app = Flask(__name__)

DATABASE = '../server/sqlite.db'

@app.route("/")
def hello():
    return render_template('base.html')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getData(table):
    connection = sqlite3.connect(DATABASE)
    connection.text_factory = str
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `%s`" % table)
    output = json.dumps(cursor.fetchall())
    connection.commit()
    connection.close()
    return output

@app.route("/api/<table>")
def parkingspots(table):
    if table == "null":
        return "[]"
    return getData(table)

@app.route("/state/")
def state():
    data = json.loads(getData('parkingspots'))
    reserved = 0
    free = 0
    occupied = 0
    for row in data:
        if row['state'] == "occupied":
            occupied += 1
        if row['state'] == "free":
            free += 1
        if row['state'] == "reserved":
            reserved += 1
    return json.dumps({"free": free, "occupied": occupied, "reserved": reserved})

@app.route("/billing/")
def billing():
    spots = json.loads(getData('parkingspots'))
    reservations = json.loads(getData('reservations'))
    prices = []
    for reservation in reservations:
        if reservation['occupiedSince'] is not None:
            start = reservation['occupiedSince']
            end = reservation['to']
            now = time.time()
            if end > now:
                diff = (now - start)
            else:
                diff = (end - start)
            price = 0
            for spot in spots:
                if reservation['parkingSpotId'] == spot['parkingSpotId']:
                    price = spot['price']
            cost = diff * price
            prices.append({'parkingSpotId': spot['parkingSpotId'], 'reservationId': reservation['reservationId'], 'cost': cost})
    return json.dumps(prices)


@app.route("/page/<page>")
def page(page):
    return render_template(page + ".html")

if __name__ == "__main__":
    app.debug = True
    app.run()