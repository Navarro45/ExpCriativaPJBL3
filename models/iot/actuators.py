from models.db import db
from models.iot.devices import Device

class Actuator(db.Model):
    __tablename__ = 'actuators'
    id = db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column(db.Integer, db.ForeignKey(Device.id))
    name = db.Column(db.String(50))  # Adicionando a coluna 'name'
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    @staticmethod
    def save_actuator(name, topic, unit, is_active):
        device = Device(name=name, is_active=is_active)
        db.session.add(device)
        db.session.commit()  # Commit aqui para obter o ID do dispositivo
        actuator = Actuator(devices_id=device.id, name=name, unit=unit, topic=topic)
        db.session.add(actuator)
        db.session.commit()

    @staticmethod
    def get_actuators():
        actuators = Actuator.query.join(Device, Device.id == Actuator.devices_id)\
            .add_columns(Device.id, Device.name, Device.is_active, Actuator.topic, Actuator.unit, Actuator.name).all()
        return actuators

    @staticmethod
    def get_single_actuator(id):
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if actuator:
            actuator = Actuator.query.filter(Actuator.devices_id == id)\
                .join(Device).add_columns(Device.id, Device.name, Device.is_active, Actuator.topic, Actuator.unit, Actuator.name).first()
            return [actuator]

    @staticmethod
    def update_actuator(id, name, topic, unit, is_active):
        try:
            device = Device.query.filter(Device.id == id).first()
            actuator = Actuator.query.filter(Actuator.devices_id == id).first()

            if device:
                print(f"Updating device: {device.id}")
                device.name = name
                device.is_active = is_active
                db.session.commit()

            if actuator:
                print(f"Updating actuator: {actuator.id}")
                actuator.name = name 
                actuator.topic = topic
                actuator.unit = unit
                db.session.commit()

        except Exception as e:
            print(f"Error updating actuator: {e}")

        return Actuator.get_actuators()

    @staticmethod
    def delete_actuator(id):
        device = Device.query.filter(Device.id == id).first()
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if actuator:
            db.session.delete(actuator)
        if device:
            db.session.delete(device)
        db.session.commit()
        return Actuator.get_actuators()
