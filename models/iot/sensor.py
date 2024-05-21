import flask_login

sensores = {'Temperatura': 0,'Umidade' : 0}

class Sensor(flask_login.UserMixin):
    pass

def get_sensors():
    global sensores
    return sensores

def add_sensor(sensor, initial_value):
    sensores[sensor] = initial_value
    return sensores

def remove_sensor(sensor):
    sensores.pop(sensor)
    return sensores
