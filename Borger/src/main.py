import datetime

from flask import Flask, request, jsonify
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
adresses_schema = AddressSchema(many=True)


# Create borger
@app.route('/api/borger', methods=['POST'])
def add_borger():
    userId = request.json['userId']

    new_borger = Borger(userId)

    db.session.add(new_borger)
    db.session.commit()

    return borger_schema.jsonify(new_borger)


# Get all borgers
@app.route('/api/borger', methods=['GET'])
def get_all_borger():
    all_borgers = Borger.query.all()
    result = borgers_schema.dump(all_borgers)
    return jsonify(result)


# Get single borger
@app.route('/api/borger/<id>', methods=['GET'])
def get_single_borger(id):
    borger = Borger.query.get(id)
    return borger_schema.jsonify(borger)


# Update borger
@app.route('/api/borger/<id>', methods=['PUT'])
def update_borger(id):
    borger = Borger.query.get(id)

    userId = request.json['userId']
    createdAt = request.json['createdAt']

    borger.userId = userId
    borger.createdAt = createdAt

    db.session.commit()

    return borger_schema.jsonify(borger)


if __name__ == '__main__':
    app.run(port=5004, debug=True)
