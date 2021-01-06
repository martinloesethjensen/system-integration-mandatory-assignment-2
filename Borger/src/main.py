import datetime
import json

from flask import Flask, request, jsonify, Response
from flask_marshmallow import Schema
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///borger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class Borger(db.Model):
    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, userId):
        self.userId = userId

    def __repr__(self):
        return '<Borger %s>' % self.userId


class BorgerSchema(Schema):
    class Meta:
        fields = ("id", "userId", "createdAt")
        model = Borger


class Address(db.Model):
    id = Column(Integer, primary_key=True)
    borgerUserId = Column(Integer, ForeignKey('borger.id'), nullable=False)
    address = Column(String(255))
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    isValid = Column(Boolean)

    def __init__(self, borgerUserId, address, isValid):
        self.borgerUserId = borgerUserId
        self.address = address
        self.isValid = isValid

    def __repr__(self):
        return '<Address %s>' % self.address


class AddressSchema(Schema):
    class Meta:
        fields = ("id", "borgerUserId", "address", "createdAt", "isValid")
        model = Address


borger_schema = BorgerSchema()
borgers_schema = BorgerSchema(many=True)

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


# Create borger
@app.route('/api/borger/borger', methods=['POST'])
def add_borger():
    userId = request.json['userId']

    new_borger = Borger(userId)

    try:
        db.session.add(new_borger)
        db.session.commit()
    except:
        db.session.rollback()
        return "Something went wrong while creating a new borger", 500

    return borger_schema.jsonify(new_borger), 201


# Get all borgers
@app.route('/api/borger/borger', methods=['GET'])
def get_all_borger():
    all_borgers = Borger.query.all()
    result = borgers_schema.dump(all_borgers)
    return jsonify(result), 200


# Get single borger
@app.route('/api/borger/borger/<id>', methods=['GET'])
def get_single_borger(id):
    borger = Borger.query.get(id)
    if borger is None:
        return "Borger with id: {} does not exist.".format(id), 404
    return borger_schema.jsonify(borger), 200


# Update borger
@app.route('/api/borger/borger/<id>', methods=['PUT'])
def update_borger(id):
    borger = Borger.query.get(id)

    userId = request.json['userId']
    createdAt = request.json['createdAt']

    if borger is None:
        return "Borger with id: {} does not exist".format(id), 404

    if userId:
        borger.userId = userId

    if createdAt:
        borger.createdAt = createdAt

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "Something went wrong while updating the borger with id: {}".format(id), 500

    return borger_schema.jsonify(borger), 200


# Delete single borger
@app.route('/api/borger/borger/<id>', methods=['DELETE'])
def delete_single_borger(id):
    borger = Borger.query.get(id)

    if borger is None:
        return "Borger with id: {} does not exist.".format(id), 404

    try:
        db.session.delete(borger)
        db.session.commit()
    except:
        return "Something went wrong while trying to delete the borger with id: {}.".format(id), 500

    return borger_schema.jsonify(borger), 200


# Create address
@app.route('/api/borger/address', methods=['POST'])
def add_address():
    borgerUserId = request.json['borgerUserId']

    if Borger.query.get(borgerUserId) is None:
        return Response(response=json.dumps(
            {"message": "Borger does not exist!"}),
            status=500,
            mimetype="application/json")

    address = request.json['address']
    isValid = request.json['isValid']

    new_address = Address(borgerUserId, address, isValid)

    try:
        db.session.add(new_address)
        db.session.commit()
    except:
        db.session.rollback()
        return "Something went wrong while creating the address", 500

    return borger_schema.jsonify(new_address), 201


# Get all addresses
@app.route('/api/borger/address', methods=['GET'])
def get_all_addresses():
    all_addresses = Address.query.all()
    result = addresses_schema.dump(all_addresses)
    return jsonify(result), 200


# Get single address
@app.route('/api/borger/address/<id>', methods=['GET'])
def get_single_address(id):
    address = Address.query.get(id)
    if address is None:
        return "Address with id {} does not exist!", 404
    return address_schema.jsonify(address), 200


# Update address
@app.route('/api/borger/address/<id>', methods=['PUT'])
def update_address(id):
    borgerUserId = request.json['borgerUserId']
    addressField = request.json['address']
    isValid = request.json['isValid']

    address = Address.query.get(id)

    if address is None:
        return "Address with id: {} does not exist.", 404

    if borgerUserId:
        address.borgerUserId = borgerUserId
    
    if addressField:
        address.address = addressField

    if isValid:
        address.isValid = isValid

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "Something went wrong while updating the address with id: {}".format(id), 500

    return address_schema.jsonify(address), 200


# Delete single address
@app.route('/api/borger/address/<id>', methods=['DELETE'])
def delete_single_address(id):
    address = Address.query.get(id)

    if address is None:
        return "Address with id: {} does not exist", 404
    
    try:
        db.session.delete(address)
        db.session.commit()
    except:
        db.session.rollback()
        return "Something went wrong while deleting the address with id: {}".format(id), 500
    
    return address_schema.jsonify(address), 200


if __name__ == '__main__':
    app.run(port=5004, host='0.0.0.0', debug=True)
