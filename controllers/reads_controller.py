from flask import Blueprint, request, render_template
from models.iot.read import Read
from models.iot.sensors import Sensor
from flask_login import login_required


read = Blueprint("read",__name__, template_folder="views")

@read.route("/history_read")
@login_required
def history_read():
    sensors = Sensor.get_sensors()
    read = {}
    return render_template("history_read.html", sensors = sensors, read = read)

@read.route("/get_read", methods=['POST'])
@login_required
def get_read():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(id, start, end)
        print(id)
        sensors = Sensor.get_sensors()
        return render_template("history_read.html", sensors = sensors, read = read)
    
@read.route('/centrala')
def centrala():
    return render_template("centrala.html")