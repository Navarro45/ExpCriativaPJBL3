from flask import Flask, render_template, request
from models.db import db, instance
import json
from flask_mqtt import Mqtt
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read
from controllers.write_controller import write
from models.iot.read import Read
from models.iot.write import Write

def create_app():
    app = Flask(__name__,
    template_folder="./views/",
    static_folder="./static/",
    root_path="./")
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    app.config['MQTT_BROKER_URL'] = 'www.mqtt-dashboard.com'
    app.config['MQTT_USERNAME'] = 'gp07' 
    app.config['MQTT_PASSWORD'] = '123123'
    app.config['MQTT_KEEPALIVE'] = 60 
    app.config['MQTT_TLS_ENABLED'] = False
    mqtt_client = Mqtt()
    mqtt_client.init_app(app)
    MQTT_TOPIC_TEMPERATURE = "expcriativatemperatura"
    MQTT_TOPIC_HUMIDITY = "expcriativahumidade"
    MQTT_TOPIC_SEND = "expcriativaenviar"
    MQTT_TOPIC_ALERT = "expcriativaalert"
    app.register_blueprint(login_, url_prefix='/')
    app.register_blueprint(user_, url_prefix='/')
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    db.init_app(app)
    @app.route('/home')
    def home():
        return render_template("home.html")

    @app.route('/logout')
    def logout():
        return render_template("login.html")
    
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
