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

        controller = CreateUserAccController()
        result, messages = controller.create_user_account(name, email, password, confirm_password, dob, phone_number)

        print(f"Result: {result}, Message: {messages}")

        if result and messages == 'Account created successfully!':
            return redirect(url_for('UserLogin_app.login_page'))
        
        return render_template('CreateUserAccount.html', message=messages)
    
    return render_template('CreateUserAccount.html')

