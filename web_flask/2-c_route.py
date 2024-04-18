#!/usr/bin/python3
"""
Build a Flask application
"""
from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    return a simple hello message
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """
    /hbnb web page
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    # Replace underscores with spaces in the text variable
    formatted_text = escape(text).replace('_', ' ')
    return f"C {formatted_text}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
