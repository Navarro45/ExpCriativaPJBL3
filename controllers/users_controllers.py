from flask import Blueprint, request, render_template, redirect, url_for
from models.user.user import User

users_ = Blueprint("users_",__name__, template_folder="views")