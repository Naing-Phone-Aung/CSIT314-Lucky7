from db import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    star_rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    agent_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)

    def __init__(self, star_rating, description, agent_id, seller_id=None, buyer_id=None):
        if 1 <= star_rating <= 5:
            self.star_rating = star_rating
        else:
            raise ValueError("Star rating must be between 1 and 5")
        self.description = description
        self.agent_id = agent_id
        self.seller_id = seller_id
        self.buyer_id = buyer_id