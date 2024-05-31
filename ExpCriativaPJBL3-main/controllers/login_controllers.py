from flask import Blueprint, request, render_template, redirect, url_for
from models.user.user import User

login_ = Blueprint("login_",__name__, template_folder="views")


@login_.route('/')
def index():
    return render_template('login.html')


@login_.user_loader
def user_loader(user):
    users = users_
    if user not in users:
        return
    user_ = models.user.user.User()
    user_.id = user
    return user_


@login_.request_loader
def request_loader(request):
    user = request.form.get('user')
    users = users_
    if user not in users:
        return
    user_ = models.user.user.User()
    user_.id = user
    return user_