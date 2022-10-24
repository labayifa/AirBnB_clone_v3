#!/usr/bin/python3
"""Objects that handle all Restful API actions for cities in a state"""

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    for city in state.cities:
        list_cities.append(city.to_dict())
    
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/city_by_id.yml', methods=['GET'])
def city_by_id(city_id):
    """Retrieve a city of object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/city_delete.yml', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/city/create_city.yml', methods=['POST'])
def create_city(state_id):
    """Create a new city object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    
    data = request.get_json()
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/city_update.yml', methods=['PUT'])
def city_update(city_id):
    """Update a city by id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
