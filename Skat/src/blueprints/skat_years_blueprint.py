import json
from flask import request, jsonify, Response, Blueprint
import sqlalchemy 
from datetime import datetime

skat_years_blueprint = Blueprint('skat_years_blueprint', __name__)

import src.models
from app import db

@skat_years_blueprint.route('/api/skat/skat-years', methods=['GET'])
def get_all_skat_years():
    all_skat_years = src.models.SkatYears.query.all()
    result = src.models.skat_years_schema.dump(all_skat_years)
    return jsonify(result), 200


# Get single skat year
@skat_years_blueprint.route('/api/skat/skat-years/<id>', methods=['GET'])
def get_single_skat_year(id):
    skat_year = src.models.SkatYears.query.get(id)
    if skat_year is None:
        return Response(response=json.dumps(
            {"message": "Skat Year with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")
    return src.models.skat_year_schema.jsonify(skat_year), 200


# Create skat year
@skat_years_blueprint.route('/api/skat/skat-years', methods=['POST'])
def create_skat_year():
    label = request.json['label']
    created_at = request.json['createdAt']
    modified_at = request.json['modifiedAt']
    start_date = request.json['startDate']
    end_date = request.json['endDate']
    is_active = request.json['isActive']

    # TODO check for null 

    new_skat_year = src.models.SkatYears(
        label, created_at, modified_at, start_date, end_date, is_active)

    try:
        db.session.add(new_skat_year)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        return Response(response=json.dumps(
                    {"message": "Integrity Error: {}".format(e)}), 
                    status=400, 
                    content_type={"Content-Type": "application/json"})
    except:
        db.session.rollback()
        return "Something went wrong while creating a new skat year", 500

    # Get all skat users and insert into skat users years
    all_skat_users = src.models.SkatUsers.query.all()
    for skat_user in all_skat_users:
        new_skat_user_year = src.models.SkatUsersYears(
            skat_user.id, new_skat_year.id, skat_user.user_id, False, 0.0)
        try:
            db.session.add(new_skat_user_year)
            db.session.commit()
        except:
            db.session.rollback()
            return "Something went wrong while creating a new skat user year", 500
          
    return src.models.skat_year_schema.jsonify(new_skat_year), 201


# Update skat year
@skat_years_blueprint.route('/api/skat/skat-years/<id>', methods=['PUT'])
def update_skat_year(id):
    label = request.json['label']
    created_at = request.json['createdAt']
    modified_at = request.json['modifiedAt']
    start_date = request.json['startDate']
    end_date = request.json['endDate']
    is_active = request.json['isActive']

    skat_year = src.models.SkatYears.query.get(id)

    if skat_year is None:
        return Response(response=json.dumps(
            {"message": "Skat Year with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")

    if label:
        skat_year.label = label
    if created_at:
        skat_year.created_at = datetime.strptime(
            created_at, "%Y-%m-%dT%H:%M:%S")
    if modified_at:
        skat_year.modified_at = datetime.strptime(
            modified_at, "%Y-%m-%dT%H:%M:%S")
    if start_date:
        skat_year.start_date = datetime.strptime(
            start_date, "%Y-%m-%dT%H:%M:%S")
    if end_date:
        skat_year.end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    if is_active is not None:
        skat_year.is_active = is_active

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "Could not commit update skat year to database.", 500

    return src.models.skat_year_schema.jsonify(skat_year), 200


# Delete a skat year
@skat_years_blueprint.route('/api/skat/skat-years/<id>', methods=['DELETE'])
def delete_skat_year(id):
    skat_year = src.models.SkatYears.query.get(id)
    if skat_year is None:
        return Response(response=json.dumps(
            {"message": "Skat Year with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")

    try:
        db.session.delete(skat_year)
        db.session.commit()
    except:
        db.session.rollback()
        return "Could not delete skat year with id {}".format(id), 500

    return src.models.skat_year_schema.jsonify(skat_year), 200

