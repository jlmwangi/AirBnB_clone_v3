#!/usr/bin/python3
"""creates a new view for place objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


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
def create_place(city_id):
    """creates a place object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if 'user_id' not in body:
        abort(400, "Missing user_id")

    if 'name' not in body:
        abort(400, "Missing name")

    user_id = body['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_place = Place(city_id=city_id, user_id=user_id, name=body['name'])
    storage.add(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a place in the storage"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    for key, value in body.items():
        if hasattr(place, key):
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict()), 200
