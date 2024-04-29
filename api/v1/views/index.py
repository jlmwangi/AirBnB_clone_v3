#!/usr/bin/python3
"""defines a function status to return a json response"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns a json response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """ retrieves the number of each objects by type"""
    stats = {}

    names = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']

    for index, class_name in enumerate(classes):
        stats[names[index]] = storage.count(class_name)

    return jsonify(stats)
