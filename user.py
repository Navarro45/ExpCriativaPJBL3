import models.iot.user
import flask_login
from flask import Blueprint, request, render_template

user= Blueprint("user",__name__, template_folder="templates")

@user.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user_id = request.form['user']
        password = request.form['password']
        users = models.iot.user.get_users()
        adm = models.iot.user.get_adm()

        if user_id in adm and adm[user_id] == password:
            return render_template('adm_home.html')
        elif user_id in users and users[user_id] == password:
            user_ = models.iot.user.User()
            user_.id = user_id
            flask_login.login_user(user_)   
            return render_template('home.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@user.route('/list_users')
def list_users():
    users = models.iot.user.get_users()
    return render_template("users.html", devices=users)

@user.route('/register_user')
def register_user():
    return render_template("register_user.html")

@user.route('/add_user', methods=['GET','POST'])
def add_user():
    global users
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        models.iot.user.add_user(user,password)
    else:
        user = request.args.get('user', None)
        password = request.args.get('password', None)
    users[user] = password
    return render_template("users.html", devices=users)

@user.route('/remove_user')
def remove_user():
    return render_template("remove_user.html",devices=users)

@user.route('/del_user', methods=['GET','POST'])
def del_user():
    global users
    if request.method == 'POST':
        print(request.form)
        user = request.form['user']
    else:
        user = request.args.get('user', None)
        models.iot.user.remove_user(user)
    return render_template("users.html", devices=users)

@user.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET':
        user_id = request.args.get('user')
        users = models.iot.user.get_users()
        if user_id in users:
            user_data = {
                'user': user_id,
                'password': users[user_id]
            }
            return render_template('edit_user.html', user=user_data)
        else:
            return "Usuário não encontrado"
    elif request.method == 'POST':
        user_id = request.form['user']
        password = request.form['password']
        models.iot.user.add_user(user_id, password)
        users = models.iot.user.get_users()
        return render_template("users.html", devices=users)