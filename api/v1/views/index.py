#!/usr/bin/python3
"""defines a function status to return a json response"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns a json response"""
    return jsonify({"status": "OK"})
