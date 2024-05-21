import flask_login

atuadores = {'Buzzer','Led'}

class Atuador(flask_login.UserMixin):
    pass

def get_actuators():
    global atuadores
    return atuadores

def add_actuator(atuador):
    atuadores.add(atuador)
    return atuadores

def remove_actuator(atuador):
    atuadores.pop()
    return atuadores
