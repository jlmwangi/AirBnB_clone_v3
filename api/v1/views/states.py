#!/usr/bin/python3
"""handles all default restful api actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    """retrieves the list of all state objects"""
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def retrieve_state(state_id):
    """retrieves a state object based on the id"""
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state object returning an empty dictionary"""
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()

        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state using request.get_json"""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    if'name' not in body:
        abort(400, "Missing name")

    new_state = State(**body)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes='False')
def update_state(state_id):
    """updates state based on the state_id"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict())
