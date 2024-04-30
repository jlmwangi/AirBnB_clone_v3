#!/usr/bin/python3
"""handles all default restful api actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    """retrieves the list of all state objects"""
    states = storage.query(State).all()
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def retrieve_state(state_id):
    """retrieves a state object based on the id"""
    state = storage.get(State, state_id)

    if state:
        return state.to_dict()
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state object returning an empty dictionary"""
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()

        return {}, 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state using request.get_json"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    key = body['name']
    if not key:
        abort(400, "Missing name")

    new_state = State(name=key)

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates state based on the state_id"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in body.items():
        if hasattr(state, key):
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
