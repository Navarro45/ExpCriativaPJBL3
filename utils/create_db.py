from flask import Flask
from models import *
from models.db import db

def create_db(app:Flask):
    with app.app_context():
        db.create_all()