from flask import render_template, Blueprint

# In boundary/admin.py
admin_app = Blueprint('admin_app', __name__)

@admin_app.route('/admin/home')
def home_page():
    return render_template('admin_home.html')
