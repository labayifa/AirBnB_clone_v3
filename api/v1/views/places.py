#!/usr/bin/python3
"""Create a new view for Place objects that handles all default RESTFul API actions"""

from crypt import methods
from email.policy import strict
from models.place import Place
from models import storage
from models.city import City
from models.user import User
from flasgger.utils import swag_from
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    cities = storage.get(City, city_id)
    list_places = []
    if not cities:
        abort(404)
    
    for place in cities.places:
        list_places.append(place.to_dict())
    
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place_by_id.yml', methods=['GET'])
def get_place_by_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    
    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/create_place.yml', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    user = storage.all(User).values()

    if not city:
        abort(404)
    
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    
    if not user:
        abort(404)
    
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    
    data = request.get_json()
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()


    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/update_place.yml', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    ignore = ['id', 'user_id','city_id', 'created_at', 'updated_at']
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

    
