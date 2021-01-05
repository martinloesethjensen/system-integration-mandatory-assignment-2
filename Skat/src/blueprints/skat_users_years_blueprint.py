import requests 
import json
from flask import request, jsonify, Response, Blueprint
from datetime import datetime

skat_users_years_blueprint = Blueprint('skat_users_years_blueprint', __name__)

import src.models
from app import db

# Get all skat users years
@skat_users_years_blueprint.route('/api/skat/skat-users-years', methods=['GET'])
def get_all_skat_users_years():
    all_skat_users_years = src.models.SkatUsersYears.query.all()
    result = src.models.skat_users_years_schema.dump(all_skat_users_years)
    return jsonify(result), 200
