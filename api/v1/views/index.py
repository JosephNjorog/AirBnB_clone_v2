#!/usr/bin/python3
""" Api status """

from api.v1.views import app_views
from flask import jsonify, request

@app_views.route('/status', methods=['GET'])
def status():
    """ return api status """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    Retrieves the number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
