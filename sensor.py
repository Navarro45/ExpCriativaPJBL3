import models.iot.sensors
from flask import Blueprint, request, render_template

sensor= Blueprint("sensor",__name__, template_folder="templates")
sensores = models.iot.sensors.get_sensors()

@sensor.route('/list_sensor')
def list_sensors():
    return render_template("sensors.html", devices= sensores)

@sensor.route('/register_sensor')
def register_sensor():
    return render_template("register_sensor.html")

@sensor.route('/add_sensor', methods=['GET','POST'])
def add_sensor():
    global sensores
    if request.method == 'POST':
        sensor = request.form['sensor']
        initial_value = request.form['initial_value']
        models.iot.sensors.add_sensor(sensor,initial_value)
    else:
        sensor = request.args.get('sensor', None)
        initial_value = request.args.get('initial_value', None)
        sensores[sensor] = initial_value
    return render_template("sensors.html", devices= sensores)

@sensor.route('/remove_sensor')
def remove_sensor():
    return render_template("remove_sensor.html",devices= sensores)

@sensor.route('/del_sensor', methods=['GET','POST'])
def del_sensor():
    global sensores
    if request.method == 'POST':
        print(request.form)
        sensor = request.form['sensor']
    else:
        sensor = request.args.get('sensor', None)
        models.iot.sensors.remove_sensor(sensor)
    return render_template("sensors.html", devices= sensores)