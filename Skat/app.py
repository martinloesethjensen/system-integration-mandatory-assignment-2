import json
from datetime import datetime
import requests

from flask import Flask, request, jsonify, Response
from flask_marshmallow import Schema
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP, Text, Float



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from src.models import *

from src.blueprints.skat_users_blueprint import skat_users_blueprint
from src.blueprints.skat_years_blueprint import skat_years_blueprint
from src.blueprints.skat_users_years_blueprint import skat_users_years_blueprint
from src.blueprints.tax_blueprint import tax_blueprint

app.register_blueprint(skat_users_blueprint)
app.register_blueprint(skat_years_blueprint)
app.register_blueprint(skat_users_years_blueprint)
app.register_blueprint(tax_blueprint)



# ----------------
# Skat Years
# ----------------

# # Get all skat years


# @app.route('/api/skat/skat-years', methods=['GET'])
# def get_all_skat_years():
#     all_skat_years = SkatYears.query.all()
#     result = skat_years_schema.dump(all_skat_years)
#     return jsonify(result), 200


# Get single skat year
@app.route('/api/skat/skat-years/<id>', methods=['GET'])
def get_single_skat_year(id):
    skat_year = SkatYears.query.get(id)
    if skat_year is None:
        return Response(response=json.dumps(
            {"message": "Skat Year with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")
    return skat_year_schema.jsonify(skat_year), 200


# Create skat year
@app.route('/api/skat/skat-years', methods=['POST'])
def create_skat_year():
    label = request.json['label']
    created_at = request.json['createdAt']
    modified_at = request.json['modifiedAt']
    start_date = request.json['startDate']
    end_date = request.json['endDate']
    is_active = request.json['isActive']

    new_skat_year = SkatYears(
        label, created_at, modified_at, start_date, end_date, is_active)

    # Get all skat users and insert into skat users years
    all_skat_users = SkatUsers.query.all()
    for skat_user in all_skat_users:
        new_skat_user_year = SkatUsersYears(
            skat_user.id, new_skat_year.id, skat_user.user_id, False, 0.0)
        db.session.add(new_skat_user_year)

    db.session.add(new_skat_year)
    db.session.commit()
    return skat_year_schema.jsonify(new_skat_year), 201


# Update skat year
@app.route('/api/skat/skat-years/<id>', methods=['PUT'])
def update_skat_year(id):
    label = request.json['label']
    created_at = request.json['createdAt']
    modified_at = request.json['modifiedAt']
    start_date = request.json['startDate']
    end_date = request.json['endDate']
    is_active = request.json['isActive']

    skat_year = SkatYears.query.get(id)

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

    db.session.commit()
    return skat_year_schema.jsonify(skat_year), 200


# Delete a skat year
@app.route('/api/skat/skat-users/<id>', methods=['DELETE'])
def delete_skat_year(id):
    skat_year = SkatYears.query.get(id)
    if skat_year is None:
        return Response(response=json.dumps(
            {"message": "Skat User with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")

    db.session.delete(skat_year)
    db.session.commit()
    return skat_year_schema.jsonify(skat_year), 200


if __name__ == '__main__':
    app.run(port=5006, host='0.0.0.0', debug=True)
