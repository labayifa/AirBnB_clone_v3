#!/usr/bin/python3
"""Create a new view for User object that handles all default RESTFul API actions"""

from crypt import methods
from email.policy import strict
from models.user import User
from flask import request, abort, make_response, jsonify
from models import storage
from flasgger.utils import swag_from
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/users/get_users.yml', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    list_users = []

    users = storage.get(User).values()
    for user in users:
        list_users.append(user.to_dict())
    
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user_by_id.yml', methods=['GET'])
def get_user_by_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)
    
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)
    
    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/create_user.yml', methods=['POST'])
def create_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    if 'email' not in request.get_json():
        abort(400, description='Missing email')
    
    if 'password' not in request.get_json():
        abort(400, description='Missing password')
    
    data = request.get_json()
    new_user = User(**data)
    new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/update_user.yml', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)
    
    if user not in request.get_json():
        abort(400, description='Not a JSON')
    
    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
