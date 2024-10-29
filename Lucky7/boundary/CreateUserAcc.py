from flask import render_template, request, Blueprint, redirect, url_for
from controller.CreateUserAccController import CreateUserAccController

CreateUserAccount_app = Blueprint('CreateUserAccount_app', __name__)

@CreateUserAccount_app.route('/CreateUserAccount', methods=['POST', 'GET'])
def create_account_page():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].lower().strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        dob = request.form["dob"]
        phone_number = request.form["phone_number"].strip()
        profile = request.form.get("profile", "buyer")  # Default to 'buyer' if no profile selected

        controller = CreateUserAccController()
        result, message = controller.create_user_account(name, email, password, confirm_password, dob, phone_number, profile=profile)

        # if result:
        #     return redirect(url_for('UserLogin_app.login_page'))

        return render_template('CreateUserAccount.html', message=message)

    # Render form without admin check
    return render_template('CreateUserAccount.html')
