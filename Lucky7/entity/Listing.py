from db import db
from datetime import datetime
from sqlalchemy import Enum as SQLAlchemyEnum

class Listing(db.Model):
    __tablename__ = 'listing'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)  # Store the Imgur link
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    # Enums for select fields
    steering_type = db.Column(SQLAlchemyEnum('Automatic', 'Manual', name='steering_type_enum'), nullable=False)
    steering_position = db.Column(SQLAlchemyEnum('Left', 'Right', name='steering_position_enum'), nullable=False)
    fuel_type = db.Column(SQLAlchemyEnum('Diesel', 'Petrol', 'Electric', name='fuel_type_enum'), nullable=False)

    horsepower = db.Column(db.Integer, nullable=False)
    previous_owners = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='listed')  # Initial status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation

    # Foreign keys
    seller_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)  # Initially empty

    def __init__(self, name, image_url, model, color, mileage, steering_type, steering_position,fuel_type, horsepower, previous_owners, description, seller_id, agent_id):
        self.name = name
        self.image_url = image_url
        self.model = model
        self.color = color
        self.mileage = mileage
        self.steering_type = steering_type
        self.steering_position = steering_position
        self.fuel_type = fuel_type
        self.horsepower = horsepower
        self.previous_owners = previous_owners
        self.description = description
        self.seller_id = seller_id
        self.agent_id = agent_id
