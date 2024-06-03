from flask import Blueprint, request, render_template, redirect, url_for
from models.user.user import User
from flask_login import login_required

users_ = Blueprint("users_",__name__, template_folder="views")

@users_.route('/userss')
@login_required
def userss():
    return render_template("users.html", devices=User.get_users())