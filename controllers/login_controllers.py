from flask import Blueprint, request, render_template, redirect, url_for
from models.user.user import User

login_ = Blueprint("login_",__name__, template_folder="views")