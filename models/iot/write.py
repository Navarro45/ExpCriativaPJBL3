from models.db import db
from models.iot.actuators import Actuator
from datetime import datetime
from models.iot.devices import Device

class Write(db.Model):
    __tablename__ = 'write'
    id= db.Column('id', db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)
    mensagem = db.Column(db.String, nullable=True)

    def save_write(topic, mensagem):
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        if actuator:
            device = Device.query.filter(Device.id == actuator.devices_id).first()
            if device and device.is_active:
                write = Write(read_datetime=datetime.now(), device_id=device.id, mensagem=mensagem)
                db.session.add(write)
                db.session.commit()

    def get_write(device_id, start, end):
        writes = Write.query.filter(
            Write.device_id == device_id,
            Write.read_datetime > start,
            Write.read_datetime < end
        ).all()
        return writes
