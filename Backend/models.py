from app import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.String(50), unique=True, nullable=False)
    dish_name = db.Column(db.String(100), nullable=False)
    image_link = db.Column(db.String(200))
    dish_price = db.Column(db.Float)
    availability = db.Column(db.Boolean, default=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dishes = db.Column(db.String(200), nullable=False)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50), default='pending')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
