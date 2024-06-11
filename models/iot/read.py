from models.db import db
from models.iot.sensors import Sensor
from datetime import datetime
from models.iot.devices import Device

# Classe para leitura dos sensores

class Read(db.Model):
    __tablename__ = 'read'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    @staticmethod
    def save_read(topic, value):
        sensor = Sensor.query.filter(Sensor.topic == topic).first()
        if sensor is None:
            print(f"No sensor found for topic {topic}")
            return

        if not sensor.is_active:
            print(f"Sensor {sensor.id} is not active")
            return

        read = Read(read_datetime=datetime.now(), device_id=sensor.devices_id, value=float(value))
        print(f"Saving read: {read}")
        db.session.add(read)
        db.session.commit()
        print(f"Read saved successfully")