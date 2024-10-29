from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from db import db
from sqlalchemy import Enum

# UserAccount model for MySQL
class UserAccount(db.Model):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    profile = db.Column(Enum('admin', 'seller', 'buyer', 'usedCarAgent', name='profile_type'), nullable=False)

    def __init__(self, name, email, password, dob, phone_number, profile='buyer'):
        self.name = name
        self.email = email
        self.set_password(password)
        self.dob = dob
        self.phone_number = phone_number
        self.profile = profile

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_account(name, email, password, confirm_password, dob, phone_number, profile='buyer'):
        existing_user = UserAccount.query.filter_by(email=email).first()
        if existing_user:
            return False, 'This email is already registered!'

        existing_phone = UserAccount.query.filter_by(phone_number=phone_number).first()
        if existing_phone:
            return False, 'This phone number is already registered!'

        if password != confirm_password:
            return False, 'Passwords do not match!'

        dob = datetime.strptime(dob, "%Y-%m-%d").date()
        today = datetime.today().date()
        age = today - dob
        if age < timedelta(days=18 * 365):
            return False, 'User needs to be over 18 years old!'

        # Create the new user account with the specified profile
        new_account = UserAccount(name=name, email=email, password=password, dob=dob, phone_number=phone_number, profile=profile)
        db.session.add(new_account)
        db.session.commit()

        return True, 'Account created successfully!'

    @staticmethod
    def verify_account(email, password):
        user = UserAccount.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            return True, user
        return False, None
