from flask import render_template, Blueprint

# In boundary/buyer.py
buyer_app = Blueprint('buyer_app', __name__)

@buyer_app.route('/buyer/home')
def home_page():
    return render_template('buyer_home.html')
