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
    MQTT_TOPIC_TEMPERATURE = "expcriativatemperatura"
    MQTT_TOPIC_HUMIDITY = "expcriativahumidade"
    MQTT_TOPIC_SEND = "expcriativaenviar"
    MQTT_TOPIC_ALERT = "expcriativaalert"
    app.register_blueprint(users_, url_prefix='/')
    app.register_blueprint(sensors_, url_prefix='/')
    app.register_blueprint(actuators_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    db.init_app(app)

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
                    return render_template('admhome.html')
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

    @app.route('/central')
    @login_required
    def central():
        global temperatura, umidade
        return render_template("central.html", temperatura=temperatura, umidade=umidade)

    @app.route('/controle', methods=['GET','POST'])
    @login_required
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
    @login_required
    def send():
        return render_template("publish.html")

    @app.route('/publish', methods=['GET', 'POST'])
    @login_required
    def remoto():
        if request.method == 'POST':
            mensagem = request.form['texto']
        mqtt_client.publish(MQTT_TOPIC_SEND, mensagem)
        return render_template("publish.html")


    @mqtt_client.on_disconnect()
    def handle_disconnect():
        print("Desconectado do Broker!")
    
    return app
