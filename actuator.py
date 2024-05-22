import models.iot.actuators
from flask import Blueprint, request, render_template

actuator= Blueprint("actuator",__name__, template_folder="templates")

@actuator.route('/list_actuator')
def list_actuator():
    return render_template("actuators.html", devices=models.iot.actuators.get_actuators())

@actuator.route('/register_actuator')
def register_actuator():
    return render_template("register_actuator.html")

@actuator.route('/add_actuator', methods=['GET','POST'])
def add_actuator():
    global atuadores
    if request.method == 'POST':
        actuator = request.form['actuator']
        models.iot.actuators.add_actuator(actuator)
    else:
        actuator = request.args.get('actuator', None)
    return render_template("actuators.html", devices=models.iot.actuators.get_actuators())

@actuator.route('/remove_actuator')
def remove_actuator():
    return render_template("remove_actuator.html",devices=models.iot.actuators.get_actuators())

@actuator.route('/del_actuator', methods=['GET','POST'])
def del_actuator():
    global atuadores
    if request.method == 'POST':
        print(request.form)
        actuator= request.form['actuator']
    else:
        actuator = request.args.get('actuator', None)
        models.iot.actuators.remove_actuator(actuator)
    return render_template("actuators.html", devices=models.iot.actuators.get_actuators())