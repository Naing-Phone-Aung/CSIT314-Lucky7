from flask import Blueprint, render_template

# In boundary/usedCarAgent.py
usedCarAgent_app = Blueprint('usedCarAgent_app', __name__)

@usedCarAgent_app.route('/usedCarAgent/home')
def home_page():
    return render_template('usedCarAgent_home.html')
