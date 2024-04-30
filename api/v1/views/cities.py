#!/usr/bin/python3
"""
creates a view of the City objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes='False')
def retrieve_cities(state_id):
    """ retrieves a list of cities of a state"""

    city_list = []
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    """ iterate over cities of a particular state"""
    for city in state.cities:
        city_list.append(city.to_dict())

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes='False')
def retrieve_city(city_id):
    """ retrieves a city object"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes='False')
def delete_city(city_id):
    """ deletes a city object"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes='False')
def create_city(state_id):
    """ creates a City object """

    """ check if state_id is linked to a state object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    """ create a city instance"""
    data['state_id'] = state_id
    city_inst = City(**data)
    city_inst.save()

    return jsonify(city_inst.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes='False')
def update_city(city_id):
    """ updates a city object"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    """ update city with the provided info """
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()

    return jsonify(city.to_dict()), 200
