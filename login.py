from flask import Blueprint, request, render_template, redirect, url_for
import models
import models.user
login = Blueprint("login",__name__, template_folder="templates")

users = models.user.get_users()

@login.route('/register_user')
def register_user():
    return render_template("register_user.html")

@login.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        models.user.add_user(user,password)
    else:
        user = request.args.get('user', None)
        password = request.args.get('password', None)
        models.user.add_user(user,password)
        
    return render_template("users.html", devices=users)

@login.route('/remove_user')
def remove_user():
    return render_template("remove_user.html",devices=users)

@login.route('/del_user', methods=['GET','POST'])
def del_user():
    if request.method == 'POST':
        print(request.form)
        user = request.form['user']
        models.user.remove_user(user)
    else:
        user = request.args.get('user', None)
        models.user.remove_user(user)
    return render_template("users.html", devices=users)