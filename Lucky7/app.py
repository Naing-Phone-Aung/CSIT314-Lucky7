from flask import Flask
from db import db
from entity.UserAccount import UserAccount

# Flask app initialization
app = Flask(__name__)
app.secret_key = "LinPyae"

# App configuration settings (including database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:linpyaehmoo@lucky7.cfi6uo08gsoq.ap-southeast-2.rds.amazonaws.com/Lucky7"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

with app.app_context():
    db.create_all()

# Import and register blueprints
from boundary.CreateUserAcc import CreateUserAccount_app 
app.register_blueprint(CreateUserAccount_app)

from boundary.UserLogin import UserLogin_app 
app.register_blueprint(UserLogin_app)

from boundary.UserLogout import UserLogout_app
app.register_blueprint(UserLogout_app)

if __name__ == "__main__":
    app.run(debug=True)
