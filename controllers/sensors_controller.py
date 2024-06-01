from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.sensors import Sensor
from flask_login import login_required

sensors_ = Blueprint("sensors_",__name__, template_folder="views")


@sensors_.route('/register_sensor')
@login_required
def register_sensor():
    return render_template("register_sensor.html")

@sensors_.route('/edit_sensor')
@login_required
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor = sensor)


@sensors_.route('/update_sensor', methods=['POST'])
@login_required
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    sensors = Sensor.update_sensor(id, name, topic, unit, is_active )
    return render_template("sensors.html", sensors = sensors)

@sensors_.route('/add_sensor', methods=['POST'])
@login_required
def add_sensor():
    name = request.form.get("name")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    
    Sensor.save_sensor(name, topic, unit, is_active )


    return render_template("sensors.html", sensors = Sensor.get_sensors())

@sensors_.route('/del_sensor', methods=['GET'])
@login_required
def del_sensor():
    id = request.args.get('id', None)
    sensors = Sensor.delete_sensor(id)
    return render_template("sensors.html", sensors = sensors)


@sensors_.route('/sensors')
@login_required
def sensors():
    
    return render_template("sensors.html",devices=Sensor.get_sensors())

@sensors_.route('/sensorsuser')
@login_required
def sensorsuser():
    return render_template("sensorsuser.html",devices=Sensor.get_sensors())

