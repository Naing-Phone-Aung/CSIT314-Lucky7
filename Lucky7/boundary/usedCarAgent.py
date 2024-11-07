from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from controller.CarListingController import AgentCreateListing, AgentUpdateListing, AgentDeleteListing, AgentSearchListing, AgentViewListing
from controller.AgentController import AgentController, AgentViewReview
from flask import jsonify


usedCarAgent_app = Blueprint('usedCarAgent_app', __name__)

@usedCarAgent_app.route('/usedCarAgent')
def home_page():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = AgentSearchListing()
    agent_id = session.get('id') 
    # Fetch listings created by the agent
    listings = controller.get_listings_by_agent(agent_id)
    
    Agentcontroller = AgentController()
    agent_detail = Agentcontroller.get_agent_detail(session.get('id'))

    if agent_detail:
        name = agent_detail.name 
    else:
        flash("Seller details not found.")
        return redirect(url_for('UserLogin_app.login_page'))

    return render_template('/usedCarAgent/agent_home.html', listings=listings, name = name)


@usedCarAgent_app.route('/usedCarAgent/create_listing', methods=['GET', 'POST'])
def create_listing():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    CreateController = AgentCreateListing()
    ListingController = AgentSearchListing()
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

        success, message = CreateController.create_listing(form_data, agent_id)

        if success:
            flash("Listing created successfully.", "success")
            # Fetch listings created by the agent

        else:
            for error in message:
                flash(error, "error")

    listings = ListingController.get_listings_by_agent(agent_id)
    Agentcontroller = AgentController()
    agent_detail = Agentcontroller.get_agent_detail(session.get('id'))

    if agent_detail:
        name = agent_detail.name 
    else:
        flash("Seller details not found.")
        return redirect(url_for('UserLogin_app.login_page'))
    return render_template('/usedCarAgent/agent_home.html', listings=listings, name = name)


@usedCarAgent_app.route('/usedCarAgent/viewListing/<int:listing_id>')
def view_listing(listing_id):
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "errror")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = AgentViewListing()
    result = controller.get_listing_details(listing_id)

    if result:
        listing, seller_name, seller_email, name = result
        return render_template('/usedCarAgent/view_listing.html', listing=listing, seller_name=seller_name, seller_email=seller_email, name=name)
    else:
        abort(404)  # Show a 404 error if the listing is not found

@usedCarAgent_app.route('/usedCarAgent/update_listing/<int:listing_id>', methods=['POST'])
def update_listing(listing_id):
    controller = AgentUpdateListing()
    # Ensure correct profile and get form data
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    form_data = {
        'name': request.form['name'],
        'color': request.form['color'],
        'steering_position': request.form['steering_position'],
        'previous_owners': request.form['previous_owners'],
        'price': request.form['price'],
        'mileage': request.form['mileage'],
        'steering_type': request.form['steering_type'],
        'model': request.form['model'],
        'horsepower': request.form['horsepower'],
        'fuel_type': request.form['fuel_type'],
        'description': request.form['description'],
    }
    if 'image' in request.files:
        form_data['image'] = request.files['image']

    # Perform the update via controller
    controller.update_listing(listing_id, form_data)
    flash("Listing updated successfully.", "success")
    return redirect(url_for('usedCarAgent_app.view_listing', listing_id=listing_id))


@usedCarAgent_app.route('/usedCarAgent/search')
def search_listings():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    search_query = request.args.get('search', '').strip()
    controller = AgentSearchListing()
    agent_id = session.get('id')  # Assuming agent ID is stored in session after login

    # Fetch all listings if no search query is provided
    listings = controller.get_listings_by_agent(agent_id, search_query)

    listings_data = [
        {
            'id': listing.id,
            'name': listing.name,
            'mileage': listing.mileage,
            'price': listing.price,
            'image_url': listing.image_url,
            'previous_owners' : listing.previous_owners,
            'created_at' : listing.created_at.strftime('%d-%m-%Y') 
        }
        for listing in listings
    ]

    return jsonify({'listings': listings_data})

@usedCarAgent_app.route('/usedCarAgent/reviews')
def view_reviews():
    # Check if the user has the correct profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    agent_id = session.get('id')  # Retrieve the agent's ID from the session
    if not agent_id:
        flash("User session has expired. Please log in again.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    # Get the filter type from the request
    filter_by = request.args.get('filter_by', 'all')  # default to 'all' if not specified

    # Fetch agent details and reviews using the controller with filter
    aController = AgentController()
    agent_detail = aController.get_agent_detail(agent_id)

    reviewController = AgentViewReview()
    reviews = reviewController.get_review_to_agent(agent_id, filter_by=filter_by)

    Agentcontroller = AgentController()
    agent_detail = Agentcontroller.get_agent_detail(session.get('id'))

    if agent_detail:
        name = agent_detail.name 
    else:
        flash("Seller details not found.")
        return redirect(url_for('UserLogin_app.login_page'))

    return render_template(
        '/usedCarAgent/view-agent-reviews.html',
        reviews=reviews,
        name=name,
        filter_by=filter_by  # Pass filter_by to maintain button state in the template
    )


@usedCarAgent_app.route('/usedCarAgent/profile')
def view_profile():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = AgentController()
    agent_detail = controller.get_agent_detail(session.get('id'))

    if agent_detail:
        name = agent_detail.name  
    else:
        flash("Agent details not found.")
        return redirect(url_for('agent_app.home_page'))
    
    return render_template('/usedCarAgent/agent_profile.html', agent_detail=agent_detail, name=name)

@usedCarAgent_app.route('/usedCarAgent/delete_listing/<int:listing_id>', methods=['POST'])
def delete_listing(listing_id):
    # Check if the user has the correct profile
    if 'profile' not in session or session['profile'] not in ['usedCarAgent', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = AgentDeleteListing()
    
    # Call the `remove_listing` method from the entity layer
    success = controller.remove_listing(listing_id)

    if success:
        flash("Listing deleted successfully.", "success")
    else:
        flash("Failed to delete listing. It may not exist.", "error")

    return redirect(url_for('usedCarAgent_app.home_page'))
