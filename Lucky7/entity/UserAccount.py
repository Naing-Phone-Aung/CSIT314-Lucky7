from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from db import db

# UserAccount model for MySQL
class UserAccount(db.Model):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, name, email, password, dob, phone_number):
        self.name = name
        self.email = email
        self.set_password(password)
        self.dob = dob
        self.phone_number = phone_number

    def set_password(self, password):
        # Generate hashed password
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        # Verify the given password
        return check_password_hash(self.password, password)

    def create_account(name, email, password, confirm_password, dob, phone_number):
        # Check if email already exists
        existing_user = UserAccount.query.filter_by(email=email).first()
        if existing_user:
            return False, 'This email is already registered!'

        # Check if phone number already exists
        existing_phone = UserAccount.query.filter_by(phone_number=phone_number).first()
        if existing_phone:
            return False, 'This phone number is already registered!'

        # Check if passwords match
        if password != confirm_password:
            return False, 'Passwords do not match!'
        
        # Change datatype of dob
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

        # Check if age is over 18 years old
        today = datetime.today().date()
        age = today - dob
        if age < timedelta(days=18*365):
            return False, 'User needs to be over 18 years old!'

        # If all checks pass, create the new user
        new_account = UserAccount(name=name, email=email, password=password, dob=dob, phone_number=phone_number)
        db.session.add(new_account)
        db.session.commit()
        
        return True, 'Account created successfully!'

    
    def verify_account(email, password):
        # Find user by email
        user = UserAccount.query.filter_by(email=email).first()

        # Verify the password
        if user and user.verify_password(password):
            return True, user.id
        return False, None

    