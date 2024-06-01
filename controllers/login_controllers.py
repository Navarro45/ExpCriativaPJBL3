from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.user.user import User
import flask_login

login_ = Blueprint("login_",__name__, template_folder="views")


@login_.route('/')
def index():
    return render_template('login.html')

@login_.route('/validated_user', methods=['POST','GET'])
def validated_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Buscar usuário pelo nome de usuário
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Comparar diretamente a senha sem hash (não recomendado)
            flask_login.login_user(user)
            return render_template('home.html')
        else:
            flash('Invalid credentials!')
            return '<h1>Invalid credentials!</h1>'
    else:
        return render_template('login.html')