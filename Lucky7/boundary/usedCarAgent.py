from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from controller.CarListingController import CarListingController
from flask import jsonify


usedCarAgent_app = Blueprint('usedCarAgent_app', __name__)

@usedCarAgent_app.route('/usedCarAgent')
def home_page():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = CarListingController()
    agent_id = session.get('id')  # Assuming agent ID is stored in session after login

    # Fetch listings created by the agent
    listings = controller.get_listings_by_agent(agent_id)

    return render_template('agent_home.html', listings=listings, name = listings[1])


@usedCarAgent_app.route('/usedCarAgent/create_listing', methods=['GET', 'POST'])
def create_listing():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
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
            flash("You must be logged in as an agent to create a listing.", "error")
            return redirect(url_for('UserLogin_app.login_page'))

        success, message = controller.create_listing(form_data, agent_id)

        if success:
            flash("Listing created successfully.", "success")
            # Fetch listings created by the agent

        else:
            for error in message:
                flash(error, "error")

    listings = controller.get_listings_by_agent(agent_id)
    return render_template('agent_home.html', listings=listings, name = listings[1])


@usedCarAgent_app.route('/usedCarAgent/viewListing/<int:listing_id>')
def view_listing(listing_id):
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "errror")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = CarListingController()
    result = controller.get_listing_details(listing_id)

    if result:
        listing, seller_name, seller_email, agent_name = result  # Unpack the Listing object and seller_name
        return render_template('view_listing.html', listing=listing, seller_name=seller_name, seller_email=seller_email, agent_name=agent_name)
    else:
        abort(404)  # Show a 404 error if the listing is not found

@usedCarAgent_app.route('/usedCarAgent/update_listing/<int:listing_id>', methods=['GET', 'POST'])
def update_listing(listing_id):
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = CarListingController()
    agent_id = session.get('id')  # Assuming agent ID is stored in session after login

    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'image': request.files.get('image'),  # image might be optional in update
            'model': request.form['model'],
            'price': request.form['price'],
            'color': request.form['color'],
            'mileage': request.form['mileage'],
            'steering_type': request.form['steering_type'],
            'steering_position': request.form['steering_position'],
            'fuel_type': request.form['fuel_type'],
            'horsepower': request.form['horsepower'],
            'previous_owners': request.form['previous_owners'],
            'description': request.form.get('description', ''),
        }

        success, message = controller.update_listing(listing_id, form_data, agent_id)

        if success:
            flash("Listing updated successfully.", "success")
            # Fetch the updated listing details to display on the same page
            result = controller.get_listing_details(listing_id)
        else:
            for error in message:
                flash(error, "error")

    if not result:
        abort(404)  # Show a 404 error if the listing is not found

    listing, seller_name, seller_email = result
    return redirect(url_for('usedCarAgent_app.view_listing', listing_id=listing_id))

@usedCarAgent_app.route('/usedCarAgent/search')
def search_listings():
    search_query = request.args.get('search', '').strip()
    controller = CarListingController()
    agent_id = session.get('id')  # Assuming agent ID is stored in session after login

    # Fetch all listings if no search query is provided
    listings = controller.get_listings_by_agent(agent_id, search_query)

    listings_data = [
        {
            'id': listing.id,
            'name': listing.name,
            'mileage': listing.mileage,
            'price': listing.price,
            'image_url': listing.image_url
        }
        for listing in listings
    ]

    return jsonify({'listings': listings_data})

@usedCarAgent_app.route('/usedCarAgent/reviews')
def view_reviews():
    return render_template('view-agent-reviews.html')
