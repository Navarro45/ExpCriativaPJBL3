from models.db import db
from models.iot.sensors import Sensor
from datetime import datetime
from models.iot.devices import Device
class Read(db.Model):
    __tablename__ = 'read'
    id= db.Column('id', db.Integer, nullable = False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable = False)
    sensors_id= db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable = False)
    value = db.Column( db.Float, nullable = True)

    def save_read(topic, value):
        sensor = Sensor.query.filter(Sensor.topic == topic).first()
        if sensor is None:
            print(f"No sensor found for topic {topic}")
            return
        
        device = Device.query.filter(Device.id == sensor.devices_id).first()
        if device is None or not device.is_active:
            print(f"No active device found for sensor {sensor.id}")
            return
        
        read = Read(read_datetime=datetime.now(), sensors_id=sensor.id, value=float(value))
        print(read)
        db.session.add(read)
        db.session.commit()

    def get_read(device_id, start, end):
        sensor = Sensor.query.filter(Sensor.devices_id == device_id).first()
        read = Read.query.filter(Read.sensors_id == sensor.id,
                                    Read.read_datetime > start,
                                    Read.read_datetime<end).all()
        return read

