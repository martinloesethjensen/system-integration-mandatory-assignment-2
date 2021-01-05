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

from src.blueprints.skat_users_blueprint import skat_users_blueprint
from src.blueprints.skat_years_blueprint import skat_years_blueprint
from src.blueprints.tax_blueprint import tax_blueprint

app.register_blueprint(skat_users_blueprint)
app.register_blueprint(skat_years_blueprint)
app.register_blueprint(tax_blueprint)

# ----------------
# Skat Users Years
# ----------------

# Get all skat users years
@app.route('/api/skat/skat-users-years', methods=['GET'])
def get_all_skat_users_years():
    all_skat_users_years = SkatUsersYears.query.all()
    result = skat_users_years_schema.dump(all_skat_users_years)
    return jsonify(result), 200


app.run(port=5006, host='0.0.0.0', debug=True)
