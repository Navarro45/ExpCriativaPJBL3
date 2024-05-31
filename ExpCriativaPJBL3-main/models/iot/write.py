from models.db import db
from models.iot.actuators import Actuator
from datetime import datetime
from models.iot.devices import Device


class Write(db.Model):
    __tablename__ = 'write'
    id= db.Column('id', db.Integer, nullable = False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable = False)
    actuator_id= db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable = False)
    value = db.Column( db.Float, nullable = True)

    def save_write(topic, value):
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        device = Device.query.filter(Device.id == actuator.devices_id).first()
        if (actuator is not None) and (device.is_active==True):
            write = Write( read_datetime = datetime.now(), actuators_id = actuator.id, value = float(value) )
            db.session.add(write)
            db.session.commit()

    def get_write(device_id, start, end):
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        write = Write.query.filter(Write.sensors_id == actuator.id,
                                    Write.read_datetime > start,
                                    Write.read_datetime<end).all()
        return write

