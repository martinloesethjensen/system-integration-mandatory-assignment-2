import json
from datetime import datetime
import requests

from flask import Flask, request, jsonify, Response
from flask_marshmallow import Schema
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP, Text, Float

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------
# Skat Users
# ----------------

# Get all skat users


@app.route('/api/skat/skat-users', methods=['GET'])
def get_all_skat_users():
    all_skat_users = SkatUsers.query.all()
    result = skat_users_schema.dump(all_skat_users)
    return jsonify(result)


# Get single skat user
@app.route('/api/skat/skat-users/<id>', methods=['GET'])
def get_single_skat_user(id):
    skat_user = SkatUsers.query.get(id)
    if skat_user is None:
        return Response(response=json.dumps(
            {"message": "Skat User with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")
    return skat_user_schema.jsonify(skat_user), 200


# Delete a skat user
@app.route('/api/skat/skat-users/<id>', methods=['DELETE'])
def delete_skat_user(id):
    skat_user = SkatUsers.query.get(id)
    if skat_user is None:
        return Response(response=json.dumps(
            {"message": "Skat User with id {} does not exist!".format(id)}),
            status=404, mimetype="application/json")

    # Delete user from skat user year table
    SkatUsersYears.query.filter_by(skat_user_id=skat_user.id).delete()

    db.session.delete(skat_user)
    db.session.commit()
    return skat_user_schema.jsonify(skat_user), 200


# Create skat user
@app.route('/api/skat/skat-users', methods=['POST'])
def create_skat_user():
    user_id = request.json['userId']
    created_at = request.json['createdAt']
    is_active = request.json['isActive']
    new_skat_user = SkatUsers(user_id, created_at, is_active)
    db.session.add(new_skat_user)
    db.session.commit()
    return skat_user_schema.jsonify(new_skat_user), 201


# Update skat user
@app.route('/api/skat/skat-users/<id>', methods=['PUT'])
def update_skat_user(id):
    user_id = request.json['userId']
    created_at = request.json['createdAt']
    is_active = request.json['isActive']

    skat_user = SkatUsers.query.get(id)

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

    db.session.commit()
    return skat_user_schema.jsonify(skat_user), 200

# ----------------
# Skat Years
# ----------------

# Get all skat years


@app.route('/api/skat/skat-years', methods=['GET'])
def get_all_skat_years():
    all_skat_years = SkatYears.query.all()
    result = skat_years_schema.dump(all_skat_years)
    return jsonify(result), 200


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


# ----------------
# Skat Users Years
# ----------------

# Get all skat users years
@app.route('/api/skat/skat-users-years', methods=['GET'])
def get_all_skat_users_years():
    all_skat_users_years = SkatUsersYears.query.all()
    result = skat_users_years_schema.dump(all_skat_users_years)
    return jsonify(result), 200


# ----------------
# Pay Taxes
# ----------------

@app.route('/api/skat/pay-taxes', methods=['POST'])
def pay_taxes():
    user_id = request.json['UserId']
    user_amount = request.json['Amount']

    skat_user_year = SkatUsersYears.query.filter_by(user_id=user_id).first()

    if not skat_user_year:
        return Response(response=json.dumps(
            {"message": "Skat User Year with user id {} does not exist!".format(user_id)}),
            status=404, mimetype="application/json")

    if skat_user_year.is_paid == 1:
        return Response(response=json.dumps(
            {"message": "Skat user has paid taxes"}),
            status=200, mimetype="application/json")
    else:
        tax_calc_response = requests.post('http://skat_tax_calculator/api/Skat_Tax_Calculator',
                                          data=json.dumps(
                                              {'amount': user_amount}),
                                          headers={'Content-Type': 'application/json'})

        # Status code is 200
        if tax_calc_response:
            json_response = tax_calc_response.json()
            tax_money = json_response['tax_money']

            # tax_money can't be negative
            # Return 400 - bad request 'cause of negative number value
            if tax_money < 0:
                return Response(response=json.dumps(
                    {"message": "Negative Value"}),
                    status=400, mimetype="application/json")

            skat_user_year.amount = tax_money
            skat_user_year.is_paid = True

            bank_response = requests.post('http://bank_system/api/Money/withdrawl',
                                          data=json.dumps(
                                              {'userId': user_id, 'amount': user_amount}),
                                          headers={'Content-Type': 'application/json'})

            # Status code is 200
            if bank_response:
                # Only commit db changes if bank_response is ok
                db.session.commit()
                return Response(response=json.dumps(
                    {"message": "Succeeded in sending request to the bank api"}),
                    status=200, mimetype="application/json")
            else:

                return Response(response=json.dumps(
                    {"message": "Something went wrong with the request for withdrawing money."}),
                    status=500, mimetype="application/json")

            return skat_user_year_schema.jsonify(skat_user_year)
        else:
            return Response(response=json.dumps(
                {"message": "Something went wrong with the request to Skat Tax Calculator."}),
                status=500, mimetype="application/json")


if __name__ == '__main__':
    app.run(port=5006, host='0.0.0.0', debug=True)
