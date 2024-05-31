from models.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., 'admin' or 'user'


    def save_user(username, email, password, role):
        user = User(username=username, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

    def get_users():
        users = User.query.all()
        return users
    
    def get_single_user(id):
        user = User.query.filter(User.id == id).first()
        return user

    def update_user(id, username=None, email=None, password=None, role=None):
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