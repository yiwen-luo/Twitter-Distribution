import flask
from flask import request
import redis
import json
import numpy as np

app = flask.Flask(__name__)
conn = redis.Redis()

def get_rate():
    return 1.0

def get_data():
    keys = conn.keys()
    # Parse data into a python dict for convenient manipulations
    items = {key: conn.mget(key)[0] for key in keys}
    # Sum of the counts for calculation of distribution
    z = sum([float(items[key]) for key in keys])
    return {key: float(items[key]) / z for key in keys}


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')


@app.route("/distribution")
def histogram():
    raw_data = get_data()
    # Just return the parsed data and return to the route "/"
    # raw_data1 = {}
    # for key in raw_data:
    #     raw_data1[key] = str(raw_data[key])
    return json.dumps(raw_data)


@app.route("/entropy")
def entropy():
    raw_data = get_data()
    # Calculate the entropy and return to the route "/entropy"
    return json.dumps({"entropy": -sum([p * np.log(p) for p in raw_data.values()])})


@app.route("/probability")
def probability():
    # Receive request from HTTP
    continent = request.args.get('continent', '')

    # Get the distribution of continents
    print continent
    d = get_data()

    # Get the count for the continent
    try:
        c = d[continent]
    except KeyError:
        return json.dumps({
            "continent": continent,
            "prob": 0.0,
        })
    # Get the normalising constant
    z = sum([float(v) for v in d.values()])
    return json.dumps({
        "continent": continent,
        "prob": float(c) / z,
    })


@app.route("/rate")
def rate():
    return json.dumps({"rate": get_rate()})


if __name__ == "__main__":
    app.debug = True
    app.run()
