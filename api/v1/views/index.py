#!/usr/bin/python3
"""API index file"""

from crypt import methods
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return API status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_count():
    """an endpoint that retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    objs_count = {}
    for i in range(len(classes)):
        objs_count[names[i]] = storage.count(classes[i])
    
    return jsonify(objs_count)
