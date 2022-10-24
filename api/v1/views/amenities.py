#!/usr/bin/python3
"""a new view for Amenity objects that handles all default RESTFul API actions"""

from crypt import methods
from email.policy import strict
from urllib import response
from models.amenity import Amenity
from flasgger.utils import swag_from
from models import storage
from flask import make_response, jsonify, request, abort
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenities.yml', methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    list_amenities = []

    amenities = storage.get(Amenity).values()
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenity_by_id.yml', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a amenity objects"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/create_amenity.yml', methods=['POST'])
def create_amenity():
    """Returns a new amenity object"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    
    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()

    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/update_amenity.yml', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(400)
    
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
