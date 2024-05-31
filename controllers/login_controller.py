from flask import Blueprint, request, render_template, redirect, url_for
from models.user.user import User
import flask_login

login_ = Blueprint("login_",__name__, template_folder="views")


@login_.route('/')
def index():
    return render_template('login.html')

@login_.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        users = User.get_users()
        if user in users and users[user] == password:
            user_ = User.get_users()
            user_.id = user
            flask_login.login_user(user_)
            return render_template('home.html')
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')