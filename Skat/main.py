import json
from datetime import datetime

from flask import Flask, request, jsonify, Response
from flask_marshmallow import Schema
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, TIMESTAMP, Text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class SkatUser(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(200), nullable=False,)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    is_active = Column(Boolean, nullable=False, default=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self

    def __repr__(self):
        return '<SkatUser %s>' % self.user_id


class SkatUserSchema(Schema):
    class Meta:
        fields = ("id", "user_id", "created_at", "is_active")
        model = SkatUser


class SkatYear(db.Model):
    id = Column(Integer, primary_key=True)
    label = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    modified_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    start_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    end_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())

    def __init__(self, label, start_date, end_date):
        self.label = label
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return '<SkatYear %s>' % self.label


class SkatYearSchema(Schema):
    class Meta:
        fields = ("id", "label", "created_at", "modified_at", "start_date", "end_date")
        model = SkatYear

class SkatUserYear(db.Model):
    id = Column(Integer, primary_key=True)
    skat_user_id = Column(Integer, ForeignKey('skat_users.id'), nullable=False)
    skat_year_id = Column(Integer, ForeignKey('skat_years.id'), nullable=False)
    user_id = Column(String(200), nullable=False,)
    is_paid = Column(Boolean, nullable=False, default=False)
    amount = Column(Integer, nullable=False, default=0)

    def __init__(self, skat_user_id, skat_year_id, user_id, is_paid, amount):
        self.skat_user_id = skat_user_id
        self.skat_year_id = skat_year_id
        self.user_id = user_id
        self.is_paid = is_paid
        self.amount = amount

    def __repr__(self):
        return '<SkatUserYear %s>' % self.id


class SkatUserYearSchema(Schema):
    class Meta:
        fields = ("id", "skat_user_id", "skat_year_id", "user_id", "is_paid", "amount")
        model = SkatUserYear


skat_user_schema = SkatUserSchema()
skat_users_schema = SkatUserSchema(many=True)

skat_year_schema = SkatYearSchema()
skat_years_schema = SkatYearSchema(many=True)

skat_user_year_schema = SkatUserYearSchema()
skat_users_years_schema = SkatUserYearSchema(many=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pay-taxes', methods=['POST'])
def pay_taxes():
    pass

if __name__ == '__main__':
    app.run(port=5006, host='0.0.0.0', debug=True)
