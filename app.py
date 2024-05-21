from flask import Flask, render_template, redirect, url_for ,request, json
from flask_mqtt import Mqtt
from login import login
import flask_login
import models.user
from user import user
from sensor import sensor
import models.sensor
import models.actuator
from actuator import actuator
app = Flask(__name__)

app.register_blueprint(login, url_prefix='/')
app.register_blueprint(user, url_prefix='/')
app.register_blueprint(sensor, url_prefix='/')
app.register_blueprint(actuator, url_prefix='/')


app.secret_key = 'd54gdh543trg@!54gdh'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users_ = models.user.get_users()
sensors_=models.sensor.get_sensors()
atuadores_=models.actuator.get_actuators()

@app.route('/')
def index():
    return render_template('login.html')


@login_manager.user_loader
def user_loader(user):
    users = users_
    if user not in users:
        return
    user_ = models.user.User()
    user_.id = user
    return user_


@login_manager.request_loader
def request_loader(request):
    user = request.form.get('user')
    users = users_
    if user not in users:
        return
    user_ = models.user.User()
    user_.id = user
    return user_

temperatura = 0
umidade = 0
alerta = ''

# Configuração MQTT
app.config['MQTT_BROKER_URL'] = 'www.mqtt-dashboard.com'
app.config['MQTT_USERNAME'] = 'gp07' 
app.config['MQTT_PASSWORD'] = '123123'
app.config['MQTT_KEEPALIVE'] = 60 
app.config['MQTT_TLS_ENABLED'] = False

# Definição dos tópicos
MQTT_TOPIC_TEMPERATURE = "expcriativatemperatura"
MQTT_TOPIC_HUMIDITY = "expcriativahumidade"
MQTT_TOPIC_SEND = "expcriativaenviar"
MQTT_TOPIC_ALERT = "expcriativaalert"

mqtt_client = Mqtt()
mqtt_client.init_app(app)

# Funções MQTT
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
  if rc == 0:
    mqtt_client.subscribe(MQTT_TOPIC_TEMPERATURE)
    mqtt_client.subscribe(MQTT_TOPIC_HUMIDITY)

    print("Conectado!")

@mqtt_client.on_message()
def handle_message(client, userdata, message):
  global temperatura, umidade, alerta
  topic = message.topic
  content = json.loads(message.payload.decode())
  if topic == MQTT_TOPIC_TEMPERATURE:
    for i in content:
      if content[i] == str:
          content.pop(i)
    temperatura = int(content['temperature'])
    if temperatura > 35:
      alerta = "Alerta! Temperatura muito alta"
      float(temperatura)
      mqtt_client.publish(MQTT_TOPIC_ALERT, alerta)
    else:
      alerta = ""
  if topic == MQTT_TOPIC_HUMIDITY:
    for i in content:
      if content[i] == str:
          content.pop(i)
    umidade = int(content['humidity'])
    if umidade < 25:
      alerta = "Alerta! Umidade muito baixa"
      float(umidade)
      mqtt_client.publish(MQTT_TOPIC_ALERT, alerta)
    else:
      alerta = ""
  else:
    alerta = ""

@mqtt_client.on_disconnect()
def handle_disconnect():
  print("Desconectado do Broker!")

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
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/logout')
def logout():
    return render_template("login.html")

@app.route('/sensors')
def sensors():
    return render_template("sensors.html",devices=sensors_)

@app.route('/sensorsuser')
def sensorsuser():
    return render_template("sensorsuser.html",devices=sensors_)

@app.route('/centrala')
def centrala():
    return render_template("centrala.html")

@app.route('/actuators')
def actuators():
    return render_template("actuators.html", devices=atuadores_)

@app.route('/actuatorsuser')
def actuatorsuser():
    return render_template("actuatorsuser.html", devices=atuadores_)

@app.route('/userss')
def userss():
    return render_template("users.html", devices=users_)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)