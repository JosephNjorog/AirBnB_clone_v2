#!/usr/bin/python3
"""
Flask application for dynamic & styled AirBnB
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close(error):
    """
    Close session after each request
    """
    storage.close()


@app.route('/hbnb_filters')
def states_cities_amenities():
    """
    Dynamic styled states, cities & amenities in AirBnB
    """
    states, amenities = storage.all(State), storage.all(Amenity)
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
