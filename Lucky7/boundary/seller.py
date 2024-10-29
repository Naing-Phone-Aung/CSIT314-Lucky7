from flask import Blueprint, render_template

# In boundary/seller.py
seller_app = Blueprint('seller_app', __name__)

@seller_app.route('/seller/home')
def home_page():
    return render_template('seller_home.html')
