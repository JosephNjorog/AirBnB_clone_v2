#!/usr/bin/python3
"""
Flask application to list states & cities
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_session(error):
    """
    Close session
    """
    storage.close()


@app.route('/states')
@app.route('/states/<id>')
def states_and_cities(id=''):
    """
    List states and cities
    """
    states = storage.all(State)
    return render_template('9-states.html', id=id, states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
