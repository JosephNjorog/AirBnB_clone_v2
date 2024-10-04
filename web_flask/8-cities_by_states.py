#!/usr/bin/python3
"""
Flask application to list cities by states
"""
from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close(request):
    """
    Close session
    """
    storage.close()


@app.route('/cities_by_states')
def cities():
    """
    List cities by states
    """
    states = [state for state in storage.all(State).values()]
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
