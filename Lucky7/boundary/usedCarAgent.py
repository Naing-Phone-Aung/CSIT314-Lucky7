from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from controller.CarListingController import CarListingController


usedCarAgent_app = Blueprint('usedCarAgent_app', __name__)

@usedCarAgent_app.route('/usedCarAgent')
def home_page():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = CarListingController()
    agent_id = session.get('id')  # Assuming agent ID is stored in session after login

    # Fetch listings created by the agent
    listings = controller.get_listings_by_agent(agent_id)

    return render_template('usedCarAgent_home.html', listings=listings)


@usedCarAgent_app.route('/usedCarAgent/create_listing', methods=['GET', 'POST'])
def create_listing():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = CarListingController()

    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'image': request.files['image'],
            'model': request.form['model'],
            'price' : request.form['price'],
            'color': request.form['color'],
            'mileage': request.form['mileage'],
            'steering_type': request.form['steering_type'],
            'steering_position': request.form['steering_position'],
            'fuel_type': request.form['fuel_type'],
            'horsepower': request.form['horsepower'],
            'previous_owners': request.form['previous_owners'],
            'description': request.form.get('description', ''),
            'seller_email': request.form['seller_email']
        }

        agent_id = session.get('id')  # Assuming agent ID is stored in session after login
        if not agent_id:
            flash("You must be logged in as an agent to create a listing.")
            return redirect(url_for('UserLogin_app.login_page'))

        success, message = controller.create_listing(form_data, agent_id)

        if success:
            flash("Listing created successfully.")
            return redirect(url_for('usedCarAgent_app.create_listing'))
        else:
            for error in message:
                flash(error)

    return render_template('car_listing_form.html')


@usedCarAgent_app.route('/usedCarAgent/viewListing/<int:listing_id>')
def view_listing(listing_id):
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = CarListingController()
    result = controller.get_listing_details(listing_id)

    if result:
        listing, seller_name = result  # Unpack the Listing object and seller_name
        return render_template('view_listing.html', listing=listing, seller_name=seller_name)
    else:
        abort(404)  # Show a 404 error if the listing is not found
