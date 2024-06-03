from flask import Blueprint, request, render_template,jsonify
from models.iot.read import Read
from models.iot.sensors import Sensor
from flask_login import login_required
from datetime import datetime


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
    id = request.form.get('id')
    start = request.form.get('start')
    end = request.form.get('end')

    print(f"Received start: {start}, end: {end}")

    if not start or not end:
        return jsonify({"error": "Start and end datetime values are required"}), 400

    try:
        start_datetime = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(end, '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DDTHH:MM"}), 400

    try:
        read = Read.get_read(id, start_datetime, end_datetime)
        return jsonify(read)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@read.route('/centrala')
def centrala():
    return render_template("centrala.html")