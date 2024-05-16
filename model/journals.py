""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Journal(db.Model):
    __tablename__ = 'journals'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _journalname = db.Column(db.String(255), unique=False, nullable=False)
    _prompt = db.Column(db.String(255), unique=True, nullable=False)
    _entry = db.Column(db.String(255), unique=False, nullable=False)
    _selfcare = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, journalname, prompt, entry, selfcare ):
        self._journalname = journalname    # variables with self prefix become part of the object,
        self._prompt = prompt
        self._entry = entry
        self._selfcare = selfcare
   
    @property
    def journalname(self):
        return self._journalname
    @journalname.setter
    def journalname(self, journalname):
        self._journalname = journalname
         
    @property
    def prompt(self):
        return self._prompt
    @prompt.setter
    def prompt(self, prompt):
        self._prompt = prompt

    @property
    def entry(self):
        return self._entry
    @entry.setter
    def entry(self, entry):
        self._entry = entry
    
    @property
    def selfcare(self):
        return self._selfcare
    @selfcare.setter
    def selfcare(self, selfcare):
        self._selfcare = selfcare
        
        
    def __str__(self):
        return json.dumps(self.read())


    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
    

    def read(self):
        return {
            "id": self.id,
            "journalname": self.journalname,
            "prompt": self.prompt,
            "entry": self.entry,
            "selfcare": self.selfcare,
            
        }
    

"""Database Creation and Testing """
# Builds working data for testing
def initJournals():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        journals = [
            Journal(journalname="Passed My Test", prompt="inspiration, perseverance", entry="I can't believe I passed my test, I'm so happy!", selfcare="listen to music"),
        ]
        """Builds sample user/note(s) data"""
        for journal in journals:
            try:
                journal.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {journal.journalname}")
            