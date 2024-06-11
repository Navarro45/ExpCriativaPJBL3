from models.db import db
from models.iot.sensors import Sensor
from datetime import datetime
from models.iot.devices import Device

# Classe para leitura dos sensores

class Read(db.Model):
    tablename = 'read'
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

        device = Device.query.get(sensor.devices_id)
        if device is None or not device.is_active:
            print(f"Device {device.id if device else 'unknown'} is not active or does not exist")
            return

        read = Read(read_datetime=datetime.now(), device_id=device.id, value=float(value))
        print(f"Saving read: {read}")
        db.session.add(read)
        db.session.commit()
        print(f"Read saved successfully")
    
    @staticmethod
    def get_read(sensor_id=None, start_datetime=None, end_datetime=None):
        query = Read.query.join(Device, Read.device_id == Device.id).join(Sensor, Device.id == Sensor.devices_id)

        if sensor_id is not None:
            query = query.filter(Sensor.id == sensor_id)
        
        if start_datetime is not None:
            query = query.filter(Read.read_datetime >= start_datetime)
        
        if end_datetime is not None:
            query = query.filter(Read.read_datetime <= end_datetime)
        return query.all()
