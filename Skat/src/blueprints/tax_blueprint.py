import requests 
import json
from flask import request, jsonify, Response, Blueprint

tax_blueprint = Blueprint('tax_blueprint', __name__)

import src.models
from app import db

@tax_blueprint.route('/api/skat/pay-taxes', methods=['POST'])
def pay_taxes():
    user_id = request.json['UserId']
    user_amount = request.json['Amount']

    skat_user_year = src.models.SkatUsersYears.query.filter_by(user_id=user_id).first()

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
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    return "Something went wrong with updating the skat user year to the database.", 500
                    
                return Response(response=json.dumps(
                    {"message": "Succeeded in sending request to the bank api"}),
                    status=200, mimetype="application/json")
            else:
                return Response(response=json.dumps(
                    {"message": "Something went wrong with the request for withdrawing money."}),
                    status=500, mimetype="application/json")

            return src.models.skat_user_year_schema.jsonify(skat_user_year)
        else:
            return Response(response=json.dumps(
                {"message": "Something went wrong with the request to Skat Tax Calculator."}),
                status=500, mimetype="application/json")