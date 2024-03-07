from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization

app = Flask(__name__)

# Configure SQLAlchemy for database management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'  # Change the database URI as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Define the JournalEntry model
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_text = db.Column(db.Text, nullable=False)

# Manually handle CORS headers for the journal entry route
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://isabellehp.github.io')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Serve the frontend
@app.route('/')
def index():
    return render_template("index.html")

# Endpoint to save journal entry
@app.route('/save-entry', methods=['POST'])
def save_entry():
    entry_text = request.json.get('entry', '')
    if entry_text.strip() != '':
        new_entry = JournalEntry(entry_text=entry_text)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Entry saved successfully'}), 200
    else:
        return jsonify({'error': 'Empty entry'}), 400

# Endpoint to retrieve journal entries
@app.route('/get-entries', methods=['GET'])
def get_entries():
    entries = JournalEntry.query.all()
    entries_list = [{'id': entry.id, 'entry_text': entry.entry_text} for entry in entries]
    return jsonify(entries_list), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
