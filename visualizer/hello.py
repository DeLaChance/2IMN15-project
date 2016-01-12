from coap.CustomClient import CustomClient
import json, time
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('base.html')

@app.route("/parkingspots.json")
def parkingspots():
    jeding = json.loads(client.get("/parkingspots", '{{"from": {}, "to": {}}}'.format(time.time(), time.time() + 1)).payload)
    print jeding
    return render_template('parkingspots.json', parkingspots=jeding)

if __name__ == "__main__":
    global client
    client = CustomClient(server=("127.0.0.1", 5683))
    app.debug = True
    app.run()