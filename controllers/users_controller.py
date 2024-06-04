from flask import Blueprint, request, render_template, redirect, url_for
from models.user.user import User
from flask_login import login_required

users_ = Blueprint("users_",__name__, template_folder="views")

@users_.route('/userss')
@login_required
def userss():
    return render_template("users.html", devices=User.get_users())

@users_.route('/edit_user', methods=['POST','GET'])
@login_required
def update_user():
    id = request.form.get("id")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")
    is_active = True if request.form.get("is_active") == "on" else False
    users = User.update_user(id, username, email, password,role , is_active )
    return render_template("users.html", users = users)

@users_.route('/del_user', methods=['GET'])
@login_required
def del_user():
    id = request.args.get('id', None)
    users = User.delete_user(id)
    return render_template("users.html", users = users)