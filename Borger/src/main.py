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

    db.session.add(new_borger)
    db.session.commit()

    return borger_schema.jsonify(new_borger)


# Get all borgers
@app.route('/api/borger/borger', methods=['GET'])
def get_all_borger():
    all_borgers = Borger.query.all()
    result = borgers_schema.dump(all_borgers)
    return jsonify(result)


# Get single borger
@app.route('/api/borger/borger/<id>', methods=['GET'])
def get_single_borger(id):
    borger = Borger.query.get(id)
    return borger_schema.jsonify(borger)


# Update borger
@app.route('/api/borger/borger/<id>', methods=['PUT'])
def update_borger(id):
    borger = Borger.query.get(id)

    userId = request.json['userId']
    createdAt = request.json['createdAt']

    borger.userId = userId
    borger.createdAt = createdAt

    db.session.commit()

    return borger_schema.jsonify(borger)


# Delete single borger
@app.route('/api/borger/borger/<id>', methods=['DELETE'])
def delete_single_borger(id):
    borger = Borger.query.get(id)
    db.session.delete(borger)
    db.session.commit()

    return borger_schema.jsonify(borger)


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

    db.session.add(new_address)
    db.session.commit()

    return borger_schema.jsonify(new_address)


# Get all addresses
@app.route('/api/borger/address', methods=['GET'])
def get_all_addresses():
    all_addresses = Address.query.all()
    result = addresses_schema.dump(all_addresses)
    return jsonify(result)


# Get single address
@app.route('/api/borger/address/<id>', methods=['GET'])
def get_single_address(id):
    address = Address.query.get(id)
    return address_schema.jsonify(address)


# Update address
@app.route('/api/borger/address/<id>', methods=['PUT'])
def update_address(id):
    address = Address.query.get(id)

    borgerUserId = request.json['borgerUserId']
    addressField = request.json['address']
    isValid = request.json['isValid']

    address.borgerUserId = borgerUserId
    address.address = addressField
    address.isValid = isValid

    db.session.commit()

    return address_schema.jsonify(address)


# Delete single address
@app.route('/api/borger/address/<id>', methods=['DELETE'])
def delete_single_address(id):
    address = Address.query.get(id)
    db.session.delete(address)
    db.session.commit()

    return address_schema.jsonify(address)


if __name__ == '__main__':
    app.run(port=5004, debug=True)
