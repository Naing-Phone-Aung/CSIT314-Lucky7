from flask import render_template, request, Blueprint, session
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
        is_verified, user = controller.verify_account(email, password)

        if is_verified:
            # Store user_id in the session
            session['id'] = user
            return render_template('Login.html', message=f'Login successful! Welcome, User ID: {user}.')
        else:
            return render_template('Login.html', message='Invalid email or password.')

    # Render the login page template
    return render_template('Login.html')
