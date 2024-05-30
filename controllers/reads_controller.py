from flask import Blueprint, request, render_template
from models.iot.read import Read
from models.iot.sensors import Sensor


read = Blueprint("read",__name__, template_folder="views")

@read.route("/history_read")
def history_read():
    sensors = Sensor.get_sensors()
    read = {}
    return render_template("history_read.html", sensors = sensors, read = read)

@read.route("/get_read", methods=['POST'])
def get_read():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(id, start, end)
        print(id)
        sensors = Sensor.get_sensors()
        return render_template("history_read.html", sensors = sensors, read = read)
    
@read.route('/central')
def central():
    global temperatura, umidade
    return render_template("central.html", temperatura=temperatura, umidade=umidade)

@read.route('/controle', methods=['GET','POST'])
def controle():
    if request.method == 'POST':
        message_type = request.form['message_type']
        if message_type == 'led':
            message = request.form['led_state']
            mqtt_client.publish(MQTT_TOPIC_ALERT, message)
        return render_template("centrala.html")
    else:
        return render_template("centrala.html")






@read.route('/centrala')
def centrala():
    return render_template("centrala.html")