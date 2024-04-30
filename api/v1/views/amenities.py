#!/usr/bin/python3
"""
creates a view of Amenity objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrive_amenities():
    """ retrieves all amenities"""

    amenity_list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        amenity_list.append(amenity)

    return jsonify(amenity_list.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrive_amenity(amenity_id):
    """ retrieves an amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes an amenity object"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """" creates a new amenity instance"""

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity_inst = Amenity(**data)
    amenity_inst.save()

    return jsonify(amenity_inst.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates an amenity object"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.values():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()

    return jsonify(amenity.to_dict(), 200)
