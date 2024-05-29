from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.sensors import Sensor


sensors_ = Blueprint("sensor_",__name__, template_folder="views")

@sensors_.route('/register_sensor')
def register_sensor():
    return render_template("register_sensor.html")

@sensors_.route('/edit_sensor')
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor = sensor)


@sensors_.route('/update_sensor', methods=['POST'])
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active )
    return render_template("sensors.html", sensors = sensors)

@sensors_.route('/add_sensor', methods=['POST'])
def add_sensor():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    
    Sensor.save_sensor(name, brand, model, topic, unit, is_active )

    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors = sensors)

@sensors_.route('/del_sensor', methods=['GET'])
def del_sensor():
    id = request.args.get('id', None)
    sensors = Sensor.delete_sensor(id)
    return render_template("sensors.html", sensors = sensors)


@sensors_.route('/sensors')
def sensors():
    return render_template("sensors.html",devices=sensors_)

@sensors_.route('/sensorsuser')
def sensorsuser():
    return render_template("sensorsuser.html",devices=sensors_)

