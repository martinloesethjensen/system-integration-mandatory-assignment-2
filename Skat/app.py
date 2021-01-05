from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from src.blueprints.skat_users_blueprint import skat_users_blueprint
from src.blueprints.skat_years_blueprint import skat_years_blueprint
from src.blueprints.skat_users_years_blueprint import skat_users_years_blueprint
from src.blueprints.tax_blueprint import tax_blueprint

app.register_blueprint(skat_users_blueprint)
app.register_blueprint(skat_years_blueprint)
app.register_blueprint(skat_users_years_blueprint)
app.register_blueprint(tax_blueprint)

if __name__ == '__main__':
    app.run(port=5006, host='0.0.0.0', debug=True)
