import json
from flask import request, jsonify, Response, Blueprint
from datetime import datetime

skat_users_blueprint = Blueprint('skat_users_blueprint', __name__)

import src.models
from app import db

# Get all skat users
@skat_users_blueprint.route('/api/skat/skat-users', methods=['GET'])
def get_all_skat_users():
    all_skat_users = src.models.SkatUsers.query.all()
    result = src.models.skat_users_schema.dump(all_skat_users)
    return jsonify(result), 200


# Get single skat user
@skat_users_blueprint.route('/api/skat/skat-users/<id>', methods=['GET'])
def get_single_skat_user(id):
    skat_user = src.models.SkatUsers.query.get(id)
    if skat_user is None:
        return Response(response=json.dumps(
            {"message": "Skat User with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")
    return src.models.skat_user_schema.jsonify(skat_user), 200


# Delete a skat user
@skat_users_blueprint.route('/api/skat/skat-users/<id>', methods=['DELETE'])
def delete_skat_user(id):
    skat_user = src.models.SkatUsers.query.get(id)
    if skat_user is None:
        return Response(response=json.dumps(
            {"message": "Skat User with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")

    # Delete user from skat user year table
    src.models.SkatUsersYears.query.filter_by(skat_user_id=skat_user.id).delete()

    try:
        db.session.delete(skat_user)
        db.session.commit()
    except:
        db.session.rollback()
        return "Could not delete skat user with id: {}".format(id), 500
    
    return src.models.skat_user_schema.jsonify(skat_user), 200


# Create skat user
@skat_users_blueprint.route('/api/skat/skat-users', methods=['POST'])
def create_skat_user():
    user_id = request.json['userId']
    created_at = request.json['createdAt']
    is_active = request.json['isActive']
    new_skat_user = src.models.SkatUsers(user_id, created_at, is_active)
    
    try:
        db.session.add(new_skat_user)
        db.session.commit()
    except:
        db.session.rollback()
        return "user_id: {} already exists".format(user_id), 409
    
    return src.models.skat_user_schema.jsonify(new_skat_user), 201


# Update skat user
@skat_users_blueprint.route('/api/skat/skat-users/<id>', methods=['PUT'])
def update_skat_user(id):
    user_id = request.json['userId']
    created_at = request.json['createdAt']
    is_active = request.json['isActive']

    skat_user = src.models.SkatUsers.query.get(id)

    if skat_user is None:
        return Response(response=json.dumps(
            {"message": "Skat user with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")

    if user_id:
        skat_user.user_id = user_id
    if created_at:
        skat_user.created_at = datetime.strptime(
            created_at, "%Y-%m-%dT%H:%M:%S")
    if is_active is not None:
        skat_user.is_active = is_active

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "user_id: {} already exists".format(user_id), 409
        
    return src.models.skat_user_schema.jsonify(skat_user), 200
