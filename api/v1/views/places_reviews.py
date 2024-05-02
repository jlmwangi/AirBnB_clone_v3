#!/usr/bin/python3
"""a new view for review that handles default restful api actions"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def retrieve_reviews(place_id):
    """retrieves a list of all review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    """iterates through reviews made"""
    reviews_list = [review.to_dict() for review in place.reviews]

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def retrieve_review(review_id):
    """retrieves a single review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    """jsonify to return a dictionary"""
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_reviews(review_id):
    """function to delete a review"""
    review = storage.get(Review, review_id)
    """check if review exists"""
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """creates a review using place id"""
    body = request.get_json()
    """check if json"""
    if not body:
        abort(400, description="Not a JSON")

    """if dict doesnt contain key user_id"""
    user_id = body.get('user_id')
    text = body.get('text')
    if not user_id:
        abort(400, "Missing user_id")
    if not text:
        abort(400, "Missing text")

    """retrieve place based on id"""
    place = storage.get(Place, place_id)
    """place_id not linked to any place"""
    if not place:
        abort(404)

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    """create a new instance of review"""
    new_review = Review(user_id=user_id, place_id=place_id, text=text)

    storage.add(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates a review object"""
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    """update review obj with provided data"""
    for key, value in body.items():
        if hasattr(review, key):
            setattr(review, key, value)

    storage.save()

    return jsonify(review.to_dict()), 200
