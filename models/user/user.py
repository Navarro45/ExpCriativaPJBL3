from models.db import db

class User(db.Model):
    __tablename__ = 'usuario'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., 'admin' or 'user'
    is_active = db.Column(db.Boolean, default=True)

    def save_user(username, email, password, role, is_active=True):
        user = User(username=username, email=email, password=password, role=role, is_active=is_active)
        db.session.add(user)
        db.session.commit()

    def get_users():
        users = User.query.all()
        return users
    
    def get_single_user(id):
        user = User.query.filter(User.id == id).first()
        return user

    def update_user(id, username=None, email=None, password=None, role=None, is_active=None):
        user = User.query.filter(User.id == id).first()
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.password = password
            if role:
                user.role = role
            if is_active is not None:
                user.is_active = is_active
            db.session.commit()
            return User.get_users()
        return None
    
    def delete_user(id):
        user = User.query.filter(User.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return User.get_users()
        return None