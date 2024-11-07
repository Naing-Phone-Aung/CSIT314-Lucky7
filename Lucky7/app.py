from flask import Flask, redirect, url_for
from flask_migrate import Migrate  
from db import db


# Flask app initialization
app = Flask(__name__)
app.secret_key = "LinPyae"


# App configuration settings (including database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:linpyaehmoo@lucky7.cfi6uo08gsoq.ap-southeast-2.rds.amazonaws.com/Lucky7"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate with the app
db.init_app(app)
migrate = Migrate(app, db)  # Add Flask-Migrate

with app.app_context():
    db.create_all()

# Import and register blueprints
from boundary.CreateUserAcc import CreateUserAccount_app
app.register_blueprint(CreateUserAccount_app)

from boundary.UserLogin import UserLogin_app
app.register_blueprint(UserLogin_app)

from boundary.UserLogout import UserLogout_app
app.register_blueprint(UserLogout_app)

from boundary.admin import admin_app
app.register_blueprint(admin_app)

from boundary.buyer import buyer_app
app.register_blueprint(buyer_app)

from boundary.seller import seller_app
app.register_blueprint(seller_app)

from boundary.usedCarAgent import usedCarAgent_app
app.register_blueprint(usedCarAgent_app)


# Redirect root URL to /login
@app.route('/')
def default_route():
    return redirect(url_for('UserLogin_app.login_page'))

if __name__ == "__main__":
    app.run(debug=True)
