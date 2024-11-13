from datetime import datetime, timedelta

from db import db
from sqlalchemy import Enum
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash


# UserAccount model for MySQL
class UserAccount(db.Model):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
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

    @staticmethod
    def get_seller_details(seller_id):
        return db.session.query(UserAccount).filter(UserAccount.id == seller_id).first()

    @staticmethod
    def get_all_agents():
        # Retrieve all agents with the profile 'usedCarAgent'
        return db.session.query(UserAccount).filter_by(profile='usedCarAgent').all()

    @staticmethod
    def get_agent_details(agent_id):
        # Retrieve details for a specific agent by ID
        return db.session.query(UserAccount).filter_by(id=agent_id, profile='usedCarAgent').first()

    @staticmethod
    def get_buyer_detail(buyer_id):
        # Retrieve details for a specific agent by ID
        return db.session.query(UserAccount).filter_by(id=buyer_id, profile='buyer').first()

    @staticmethod
    def validate_seller_email(email):
        # Check if a seller exists by email and return the seller's ID
        seller = db.session.query(UserAccount).filter_by(email=email, profile='seller').first()
        return seller.id if seller else None

    @staticmethod
    def get_all_accounts():
        try:
            # Retrieve all accounts except those with the name "Deleted_Account"
            accounts = db.session.query(UserAccount).filter(UserAccount.name != "Deleted_Account").all()
            return accounts
        except SQLAlchemyError:
            db.session.rollback()
            return None, "An error occurred while retrieving accounts."



    @staticmethod
    def get_admin_detail(admin_id):
    # Fetches profile information of a specific admin
        return db.session.query(UserAccount).filter_by(id=admin_id, profile='admin').first()
    
    @staticmethod
    def get_filtered_accounts(search_query='', profile_filter=''):
        query = db.session.query(UserAccount)

        # Exclude accounts with the name "Deleted_Account"
        query = query.filter(
            (UserAccount.name != "Deleted_Account") &
            (UserAccount.profile != "admin")
        )

        if search_query:
            query = query.filter(UserAccount.name.ilike(f"%{search_query}%"))

        if profile_filter:
            query = query.filter(UserAccount.profile == profile_filter)

        return query.all()



    @staticmethod
    def get_account_by_id(account_id):
        account = UserAccount.query.get(account_id)
        if account:
            acc_detail = {
                "id": account.id,
                "name": account.name,
                "email": account.email,
                "dob": account.dob,
                "phone_number": account.phone_number,
                "profile" : account.profile
            }
            return acc_detail
        return None


    @staticmethod
    def update_account_info(account_id, name, email, dob, phone_number, profile):
        user = UserAccount.query.get(account_id)
        if not user:
            return False, "User not found."

        # Check if the email is already used by another user
        email_exists = UserAccount.query.filter(UserAccount.email == email, UserAccount.id != account_id).first()
        if email_exists:
            return False, "Email is already in use by another account."

        # Check if the phone number is already used by another user
        phone_exists = UserAccount.query.filter(UserAccount.phone_number == phone_number, UserAccount.id != account_id).first()
        if phone_exists:
            return False, "Phone number is already in use by another account."

        # Validate the profile type (if necessary)
        valid_profiles = {"seller", "buyer", "usedCarAgent", "admin"}
        if profile not in valid_profiles:
            return False, "Invalid profile type selected."

        # Update user details if checks pass
        user.name = name
        user.email = email
        user.dob = dob
        user.phone_number = phone_number
        user.profile = profile  # Update the profile
        db.session.commit()
        return True, "Account updated successfully."


    @staticmethod
    def delete_account(account_id):
        account = UserAccount.query.get(account_id)
        if not account:
            return False, "Account not found."
        try:
            # Anonymize account data instead of deleting
            account.name = "Deleted_Account"
            account.email = None
            account.phone_number = None
            account.password = None
            account.dob = None
            db.session.commit()
            return True, "Account deleted successfully."
        except SQLAlchemyError:
            db.session.rollback()
            return False, "An error occurred while deleting the account."


    @staticmethod
    def reset_password(account_id, new_password, confirm_password):
        # Fetch user
        user = UserAccount.query.get(account_id)
        if not user:
            return False, "User not found."

        # Check if passwords match
        if new_password != confirm_password:
            return False, "Passwords do not match."

        # Set and save new password
        user.set_password(new_password)
        db.session.commit()
        return True, "Password reset successfully."
