import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.journals import Journal

journal_api = Blueprint('journal_api', __name__,
                   url_prefix='/api/journals')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(journal_api)

class JournalAPI:        
    class _Read(Resource):
        def get(self):
            journals = Journal.query.all()
            json_ready = [journal.read() for journal in journals]
            re = jsonify(json_ready)
            return re
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate name
            journalname = body.get('journalname')
            #if recipename is None or len(recipename) < 2:
             #   return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            prompt = body.get('promot')
            #if healthyingredients is None or len(healthyingredients) < 2:
               # return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password
            entry = body.get('entry')
            selfcare = body.get('selfcare')
            #if difficulty is None or len(difficulty) < 2:
             #   return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            journal = Journal(journalname=journalname, prompt=prompt, entry=entry, selfcare = selfcare)
            ''' Additional garbage error checking '''
                
            ''' #2: Key Code block to add user to database '''
            # create user in database
            journal = journal.create()
            # success returns json of user
            if journal:
                #return jsonify(user.read())
                return journal.read()    
            # failure returns error
            return {'message': f'Processed {journalname}, either a format error or '}, 400

        def get(self): # Read Method, the _         indicates current_user is not used
            journals = Journal.query.all()    # read/extract all users from database
            json_ready = [journal.read() for journal in journals]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
                
                    
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            journalname = body.get('journalname')
            prompt = body.get('prompt')
            entry = body.get('entry')
            selfcare = body.get('selfcare')
            new_journal = Journal(journalname=journalname, prompt=prompt, entry=entry, selfcare=selfcare)
            journal = new_journal.create()
            # success returns json of user
            return jsonify(new_journal.read()) 


            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Read, '/read')
    api.add_resource(_Create, '/make')