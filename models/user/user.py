import flask_login
from models.db import db

class User(flask_login.UserMixin):
    def get_adm():
        global adm
        return adm

    def get_users():
        global users
        return users

    def add_user(user, password):
        users[user] = password
        return users

    def remove_user(user):
        users.pop(user)
        return users

