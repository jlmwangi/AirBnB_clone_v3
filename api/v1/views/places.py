#!/usr/bin/python3
"""creates a new view for place objects"""

from api.vi.views import app_views
from flask import abort, jsonify
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def retrieve_places(city_id):
    """retrieves list of all place objects of a city"""
    places_list = []
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places_list = [place.to_dict() for place in city.places]

    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def retrieve_place(place_id):
    """retrieves a place based on the place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
