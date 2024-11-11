from flask import render_template, request, Blueprint, session, redirect, url_for
from controller.UserLoginController import UserLoginController

# Define a Blueprint for the login functionality
UserLogin_app = Blueprint('UserLogin_app', __name__)

@UserLogin_app.route('/Login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        # Get email and password from the form
        email = request.form['email'].strip().lower()
        password = request.form['password']

        # Call the LoginController to verify the credentials
        controller = UserLoginController()
        is_verified, user_id, profile = controller.verify_account(email, password)

        if is_verified:
            # Store user_id and profile in the session
            session['id'] = user_id
            session['profile'] = profile

            # Redirect based on the profile type
            if profile == 'admin':
                return redirect(url_for('admin_app.home_page'))
            elif profile == 'seller':
                return redirect(url_for('seller_app.home_page'))
            elif profile == 'buyer':
                return redirect(url_for('buyer_app.home_page'))
            elif profile == 'usedCarAgent':
                return redirect(url_for('usedCarAgent_app.home_page'))
            else:
                return render_template('Login.html', message='Unknown profile type.')

        else:
            return render_template('Login.html', message='Invalid email or password.')

    # Render the login page template
    return render_template('Login.html')

@UserLogin_app.route('/terms&conditions')
def termsNconditions():
    return render_template('terms&conditions.html')