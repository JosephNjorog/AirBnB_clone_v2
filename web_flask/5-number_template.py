#!/usr/bin/python3
"""
Build a Flask application
"""
from flask import Flask, render_template

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
    return "Python is {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def number(n):
    """
    Custom int number
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>')
def template_number(n):
    """
    Custom template int number
    """
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
