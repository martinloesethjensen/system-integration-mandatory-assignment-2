import json
import requests

from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_marshmallow import Schema
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, TIMESTAMP, Text, Float

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class SkatUsers(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(200), nullable=False,)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    is_active = Column(Boolean, nullable=False, default=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self

    def __repr__(self):
        return '<SkatUsers %s>' % self.user_id


class SkatUsersSchema(Schema):
    class Meta:
        fields = ("id", "user_id", "created_at", "is_active")
        model = SkatUsers


class SkatYears(db.Model):
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
        return '<SkatYears %s>' % self.label


class SkatYearsSchema(Schema):
    class Meta:
        fields = ("id", "label", "created_at", "modified_at", "start_date", "end_date")
        model = SkatYears

class SkatUsersYears(db.Model):
    id = Column(Integer, primary_key=True)
    skat_user_id = Column(Integer, ForeignKey('skat_users.id'), nullable=False)
    skat_year_id = Column(Integer, ForeignKey('skat_years.id'), nullable=False)
    user_id = Column(String(200), nullable=False,)
    is_paid = Column(Boolean, nullable=False, default=False)
    amount = Column(Float, nullable=False, default=0.0)

    def __init__(self, skat_user_id, skat_year_id, user_id, is_paid, amount):
        self.skat_user_id = skat_user_id
        self.skat_year_id = skat_year_id
        self.user_id = user_id
        self.is_paid = is_paid
        self.amount = amount

    def __repr__(self):
        return '<SkatUsersYears %s>' % self.id


class SkatUsersYearsSchema(Schema):
    class Meta:
        fields = ("id", "skat_user_id", "skat_year_id", "user_id", "is_paid", "amount")
        model = SkatUsersYears


skat_user_schema = SkatUsersSchema()
skat_users_schema = SkatUsersSchema(many=True)

skat_year_schema = SkatYearsSchema()
skat_years_schema = SkatYearsSchema(many=True)

skat_user_year_schema = SkatUsersYearsSchema()
skat_users_years_schema = SkatUsersYearsSchema(many=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Get all skat users
@app.route('/api/skat-users', methods=['GET'])
def get_all_skat_users():
    all_skat_users = SkatUsers.query.all()
    result = skat_users_schema.dump(all_skat_users)
    return jsonify(result)

# Get all skat years
@app.route('/api/skat-years', methods=['GET'])
def get_all_skat_years():
    all_skat_years = SkatYears.query.all()
    result = skat_years_schema.dump(all_skat_years)
    return jsonify(result)

# Get all skat users years
@app.route('/api/skat-users-years', methods=['GET'])
def get_all_skat_users_years():
    all_skat_users_years = SkatUsersYears.query.all()
    result = skat_users_years_schema.dump(all_skat_users_years)
    return jsonify(result)

@app.route('/pay-taxes', methods=['POST'])
def pay_taxes():
    user_id = request.json['UserId']
    user_amount = request.json['Amount']

    skat_user_year = SkatUsersYears.query.filter_by(user_id=user_id).first()

    print(skat_user_year)
    if skat_user_year is None:
        return Response(response=json.dumps(
            {"message": "Skat User Year does not exist!"}),
            status=500, mimetype="application/json")
    
    if skat_user_year.is_paid == 1:
        return Response(response=json.dumps(
            {"message": "Skat user has paid taxes"}),
            status=200, mimetype="application/json")
    else:
        response = requests.post('http://skat_tax_calculator/api/Skat_Tax_Calculator', 
            data=json.dumps({'amount': user_amount}), 
            headers={'Content-Type': 'application/json'})
        
        if response:
            json_response = response.json()
            tax_money = json_response['tax_money']

            if tax_money < 0:
                return Response(response=json.dumps(
                    {"message": "Negative Value"}),
                    status=500, mimetype="application/json")
            
            skat_user_year.amount = tax_money
            skat_user_year.is_paid = True

            db.session.commit()

            bank_response = requests.post('http://bank_system/api/Money/withdrawl', 
                data=json.dumps({'money': user_amount}), 
                headers={'Content-Type': 'application/json'})

            if bank_response:
                return Response(response=json.dumps(
                    {"message": "Succeeded in sending request to the bank api"}),
                    status=200,mimetype="application/json")
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
