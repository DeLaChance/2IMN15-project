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

@app.route("/page/<page>")
def page(page):
    return render_template(page + ".html")

if __name__ == "__main__":
    app.debug = True
    app.run()