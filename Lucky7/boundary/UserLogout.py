from flask import redirect, session, Blueprint

UserLogout_app = Blueprint('UserLogout_app', __name__)

@UserLogout_app.route("/Logout", methods=["POST", "GET"])
def logout_page():
    session.clear()
    return redirect('/')  