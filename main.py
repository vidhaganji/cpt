from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from api.shopping import Predict

app = Flask(__name__)

# Register CORS for cross-origin requests
CORS(app, supports_credentials=True, origins=['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io'])

api = Api(app)

# Register API resource
api.add_resource(Predict, '/api/shopping/predict')

# Error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Home route
@app.route('/')
def index():
    return render_template("index.html")

# Table route
@app.route('/table/')
def table():
    return render_template("table.html")

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")

import threading

# import "packages" from flask
from flask import render_template,request, jsonify  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization

# Import necessary modules from the project
from __init__ import app, db
from api.user import user_api
from api.journal import journal_api
from model.journals import initJournals

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

#class Quote(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    quote_text = db.Column(db.String(255), nullable=False)
#    quote_author = db.Column(db.String(100), nullable=False)
#    user_opinion = db.Column(db.Text, nullable=False)


# Register URIs
app.register_blueprint(user_api)
app.register_blueprint(journal_api)


@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.route('/api/users/save_settings', methods=['POST'])  # Define the route for saving settings
def save_settings():
    try:
        # Extract settings data from the request
        settings = request.json.get('settings')

        # Update the user's settings in the database (replace 'current_user' with your actual user object)
        # Example: current_user.update_settings(settings)
        # Make sure to implement this method in your User model

        return jsonify({'message': 'Settings saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://127.0.0.1:4100', 'http://127.0.0.1:4100', 'https://jplip.github.io']:
        cors._origins = allowed_origin
        
# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    #initUsers()
    initJournals()


# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# Run the application on the development server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port="8086")