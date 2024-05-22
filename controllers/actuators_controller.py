from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.actuators import Actuator

actuator_ = Blueprint("actuator_",__name__, template_folder="views")

@actuator_.route('/register_actuator')
def register_actuator():
    return render_template("register_actuator.html")


@actuator_.route('/add_actuator', methods=['POST'])
def add_actuator():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    
    Actuator.save_actuator(name, brand, model, topic, unit, is_active )

    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators = actuators)

@actuator_.route('/edit_actuator')
def edit_actuator():
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)
    print(actuator)
    return render_template("update_actuator.html", actuator = actuator)


@actuator_.route('/update_actuator', methods=['POST'])
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    actuators = Actuator.update_actuator(id, name, brand, model, topic, unit, is_active )
    return render_template("actuators.html", actuators = actuators)

@actuator_.route('/del_actuator', methods=['GET'])
def del_actuator():
    id = request.args.get('id', None)
    actuators = Actuator.delete_actuator(id)
    return render_template("actuators.html", actuators = actuators)

@actuator_.route('/actuators')
def actuators():
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators = actuators)