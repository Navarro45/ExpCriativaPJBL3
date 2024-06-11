from flask import Flask, render_template, request, flash
from models.db import db, instance
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mqtt import Mqtt
from controllers.sensors_controller import sensors_
from controllers.actuators_controller import actuators_
from controllers.reads_controller import read
from controllers.write_controller import write
from controllers.users_controller import users_
from models.iot.read import Read
from models.iot.write import Write
from models.user.user import User
from models.iot.sensors import Sensor
from models.iot.actuators import Actuator
from datetime import datetime


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
    login_manager = LoginManager(app)

    
    app.register_blueprint(users_, url_prefix='/')
    app.register_blueprint(sensors_, url_prefix='/')
    app.register_blueprint(actuators_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    db.init_app(app)

    # Variáveis globais para tópicos
    TOPICOS_SENSOR = {}
    TOPICOS_ALERT = {}

    def load_topics():
        global TOPICOS_SENSOR, TOPICOS_ALERT
        sensors = Sensor.get_sensors()
        actuators = Actuator.query.all()

        TOPICOS_SENSOR = {sensor.topic: sensor for sensor in sensors}
        TOPICOS_ALERT = {actuator.topic: actuator for actuator in actuators}


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/validated_user', methods=['POST','GET'])
    def validated_user():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            
            if user and user.password == password:  
                if user.role == "user":
                    login_user(user)
                    return render_template('home.html')
                elif user.role == "admin" or user.role == "adm":
                    login_user(user)
                    return render_template('adm_home.html')
                else:
                    return render_template('login.html')
            else:
                flash('Invalid credentials!')
                return '<h1>Invalid credentials!</h1>'
        else:
            return render_template('login.html')

    @app.route('/home')
    @login_required
    def home():
        return render_template("home.html")

    @app.route('/sobre')
    @login_required
    def sobre():
        return render_template('sobre.html')

    @app.route('/admhome')
    @login_required
    def admhome():
        return render_template("adm_home.html")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return render_template('login.html')
    
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            for topic in TOPICOS_SENSOR.keys():
                mqtt_client.subscribe(topic)
            for topic in TOPICOS_ALERT.keys():
                mqtt_client.subscribe(topic)
        print("Conectado!")


    @mqtt_client.on_message()
    def handle_message(client, userdata, message):
        with app.app_context():
            topic = message.topic
            content = json.loads(message.payload.decode())
            
            if topic in TOPICOS_SENSOR:
                sensor = TOPICOS_SENSOR[topic]
                if 'temperature' in content:
                    temperatura = int(content['temperature'])
                    Read.save_read(topic, temperatura)

                    if temperatura > 35:
                        alerta = "Alerta! Temperatura muito alta"
                        mqtt_client.publish(TOPICOS_ALERT.get('alert_topic', ''), alerta)

                if 'humidity' in content:
                    umidade = int(content['humidity'])
                    Read.save_read(topic, umidade)

                    if umidade < 25:
                        alerta = "Alerta! Umidade muito baixa"
                        mqtt_client.publish(TOPICOS_ALERT.get('alert_topic', ''), alerta)
            elif topic in TOPICOS_ALERT:
                actuator = TOPICOS_ALERT[topic]
                mensagem = content.get('value')
                Write.save_write(topic, mensagem)



    @app.route('/central')
    @login_required
    def central():
        return render_template("central.html")

    @app.route('/controle', methods=['GET', 'POST'])
    @login_required
    def controle():
        if request.method == 'POST':
            message_type = request.form['message_type']
            if message_type == 'led':
                message = request.form['led_state']
                Write.save_write(TOPICOS_ALERT, message)
                mqtt_client.publish(TOPICOS_ALERT, message)
            return render_template("central.html")
        else:
            sensor_id = request.args.get('sensor_id', default=1, type=int)
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

            temperatura = None
            umidade = None

            readings = Read.get_read(sensor_id, start, end)
            for reading in readings:
                if reading.unit == 'temperature':
                    temperatura = reading.value
                elif reading.unit == 'humidity':
                    umidade = reading.value

            return render_template("central.html", temperatura=temperatura, umidade=umidade)
        
    @app.route('/send', methods=['GET','POST'])
    @login_required
    def send():
        return render_template("publish.html")

    @app.route('/publish', methods=['POST'])
    @login_required
    def publish():
        mensagem = request.form['texto']
        topic = "expcriativaenviar"
        Write.save_write(topic, mensagem)
        mqtt_client.publish(topic, mensagem)
        return render_template("publish.html")



    @mqtt_client.on_disconnect()
    def handle_disconnect():
        print("Desconectado do Broker!")
    
    return app
