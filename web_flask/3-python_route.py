#!/usr/bin/python3
"""
Build a Flask application
"""
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """
    return a simple hello message
    """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """
    /hbnb web page
    """
    return "HBNB"


@app.route('/c/<text>')
def c_route(text):
    """
    Custom C urls
    """
    return "C is {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def py_route(text="is cool"):
    """
    Custom python urls
    """
    return "Python {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
