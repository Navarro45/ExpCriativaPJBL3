from flask import Flask, render_template, redirect, url_for ,request, json
from flask_mqtt import Mqtt
from login import login
import flask_login
import models.user.user
import models.iot.sensors
import models.iot.actuators
app = Flask(__name__)




app.secret_key = 'd54gdh543trg@!54gdh'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users_ = models.user.user.get_users()
sensors_=models.iot.sensors.get_sensors()
atuadores_=models.iot.actuators.get_actuators()

@app.route('/')
def index():
    return render_template('login.html')


@login_manager.user_loader
def user_loader(user):
    users = users_
    if user not in users:
        return
    user_ = models.user.user.User()
    user_.id = user
    return user_


@login_manager.request_loader
def request_loader(request):
    user = request.form.get('user')
    users = users_
    if user not in users:
        return
    user_ = models.user.user.User()
    user_.id = user
    return user_


@app.route('/central')
def central():
  global temperatura, umidade
  return render_template("central.html", temperatura=temperatura, umidade=umidade)

@app.route('/controle', methods=['GET','POST'])
def controle():
  if request.method == 'POST':
    message_type = request.form['message_type']
    if message_type == 'led':
        message = request.form['led_state']
        mqtt_client.publish(MQTT_TOPIC_ALERT, message)
    return render_template("centrala.html")
  else:
    return render_template("centrala.html")

@app.route('/send', methods=['GET','POST'])
def send():
    return render_template("publish.html")

@app.route('/publish', methods=['GET', 'POST'])
def remoto():
  if request.method == 'POST':
    mensagem = request.form['texto']
    mqtt_client.publish(MQTT_TOPIC_SEND, mensagem)
  return render_template("publish.html")

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/admhome')
def admhome():
    return render_template("adm_home.html")




@app.route('/centrala')
def centrala():
    return render_template("centrala.html")



@app.route('/userss')
def userss():
    return render_template("users.html", devices=users_)


from controllers.app_controller import create_app
from utils.create_db import create_db

if __name__ == "__main__":
    app = create_app()
    create_db(app)
    app.run(host='0.0.0.0', port=8080, debug=False)