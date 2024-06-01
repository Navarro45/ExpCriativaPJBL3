from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.actuators import Actuator

actuators_ = Blueprint("actuators_", __name__, template_folder="views")

@actuators_.route('/register_actuator')
def register_actuator():
    return render_template("register_actuator.html")

@actuators_.route('/add_actuator', methods=['POST'])
def add_actuator():
    name = request.form.get("name")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    
    Actuator.save_actuator(name, topic, unit, is_active)
    return redirect(url_for('actuators_.actuators'))

@actuators_.route('/edit_actuator')
def edit_actuator():
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)
    return render_template("update_actuator.html", actuator=actuator)

@actuators_.route('/update_actuator', methods=['POST'])
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    Actuator.update_actuator(id, name, topic, unit, is_active)
    return redirect(url_for('actuators_.actuators'))

@actuators_.route('/del_actuator', methods=['GET'])
def del_actuator():
    id = request.args.get('id', None)
    Actuator.delete_actuator(id)
    return redirect(url_for('actuators_.actuators'))

@actuators_.route('/actuators')
def actuators():
    return render_template("actuators.html", devices=Actuator.get_actuators())

@actuators_.route('/actuatorsuser')
def actuatorsuser():
    return render_template("actuatorsuser.html", devices=Actuator.get_actuators())
