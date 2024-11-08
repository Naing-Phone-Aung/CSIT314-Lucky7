from flask import flash, redirect, render_template, Blueprint, session, url_for, request
from controller.AdminController import AdminController, SearchAccount, SuspendAccount, UpdateAccount, ViewAccount
from controller.CreateUserAccController import CreateUserAccController

# Initialize Blueprint
admin_app = Blueprint('admin_app', __name__)

@admin_app.route('/admin')
def home_page():
    if 'profile' not in session or session['profile'] not in ['admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    # Retrieve search and filter criteria from query parameters
    search_query = request.args.get('search', '').strip()
    profile_filter = request.args.get('filter', '').strip()

    # Fetch filtered accounts and admin profile
    accounts = SearchAccount.get_filtered_accounts(search_query, profile_filter)
    admin_profile = AdminController.get_profile_info(session['id'])

    # Render the template with the fetched data
    return render_template(
        'admin/admin_home.html',
        accounts=accounts,
        admin_profile=admin_profile,
        name=admin_profile.name
    )

@admin_app.route('/admin/profile')
def view_profile():
    if 'profile' not in session or session['profile'] not in ['admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    admin_detail = AdminController.get_profile_info(session['id'])

    return render_template('/admin/admin_profile.html', admin_detail=admin_detail, name = admin_detail.name)

@admin_app.route('/admin/create_acc', methods=['POST', 'GET'])
def create_account_page():
    if 'profile' not in session or session['profile'] not in ['admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))
    
    admin_detail = AdminController.get_profile_info(session['id'])

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

        return render_template('/admin/create_acc.html', result=result, message=message , name=admin_detail.name)

    # Render form without admin check
    return render_template('/admin/create_acc.html', name=admin_detail.name)

@admin_app.route('/admin/account/<int:account_id>')
def account_detail(account_id):
    if 'profile' not in session or session['profile'] != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    account_detail = ViewAccount.get_account_detail(account_id)
    admin_detail = AdminController.get_profile_info(session['id'])

    if not account_detail:
        flash("Account not found.")
        return redirect(url_for('admin_app.home_page'))

    return render_template('admin/view_acc.html', account_detail=account_detail, name = admin_detail.name)


@admin_app.route('/admin/account/update/<int:account_id>', methods=['POST'])
def update_account(account_id):
    if 'profile' not in session or session['profile'] != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    # Retrieve form data
    name = request.form['name']
    email = request.form['email']
    dob = request.form['dob']
    phone_number = request.form['phone_number']
    profile = request.form['profile']  # Get profile from form

    # Call controller to update the account
    success, message = UpdateAccount.update_account(account_id, name, email, dob, phone_number, profile)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_app.account_detail', account_id=account_id))



@admin_app.route('/admin/account/delete/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    # Check if user has admin privileges
    if 'profile' not in session or session['profile'] != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    # Debug message to check if route is being hit
    print(f"Attempting to delete account with ID: {account_id}")

    # Attempt to delete the account
    success, message = SuspendAccount.delete_account(account_id)
    flash(message, 'success' if success else 'error')
    
    return redirect(url_for('admin_app.home_page'))

@admin_app.route('/admin/account/reset_password/<int:account_id>', methods=['POST'])
def reset_password(account_id):
    if 'profile' not in session or session['profile'] != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Transfer data to the entity layer for validation and update
    success, message = UpdateAccount.reset_password(account_id, new_password, confirm_password)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_app.account_detail', account_id=account_id))

