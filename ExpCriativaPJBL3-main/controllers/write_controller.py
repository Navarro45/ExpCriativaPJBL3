from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuators import Actuator

write = Blueprint("write",__name__, template_folder="views")

@write.route("/history_write")
def history_write():
    actuators = Actuator.get_actuators()
    write = {}
    return render_template("history_write.html", actuators = actuators, write = write)

@write.route("/get_write", methods=['POST'])
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Write.get_write(id, start, end)
        actuators = Actuator.get_actuators()
        return render_template("history_write.html", actuators = actuators, write = write)

@write.route('/send', methods=['GET','POST'])
def send():
    return render_template("publish.html")

@write.route('/publish', methods=['GET', 'POST'])
def remoto():
  if request.method == 'POST':
    mensagem = request.form['texto']
    mqtt_client.publish(MQTT_TOPIC_SEND, mensagem)
  return render_template("publish.html")
