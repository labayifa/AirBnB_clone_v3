#!/usr/bin/python
"""objects that handles all default RESTFul API actions"""

from crypt import methods
from email.policy import strict
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """Retrieves list of state objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['GET'])
def get__id_state(state_id):
    """Return a specific state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    return jsonify(state.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/create_state.yml', methods=['POST'])
def create_state():
    """Create a new state and return a 201 success"""
    if not request.get_json():
        abort(404, description="Not a JSON")
    
    if 'name' not in request.get_json():
        abort(404, description="Missing name")
    
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/update_state.yml', methods=['PUT'])
def update_state(state_id):
    """Update a state by id"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    
    if not request.get_json():
        abort(404, description="Not a JSON")
    
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)

