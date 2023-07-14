from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from sqlalchemy import create_engine

app = Flask(__name__)

# MySQL configuration
# app.config['MYSQL_DATABASE_USER'] = 'ujrghqg0ika5puwyz8fp'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'pscale_pw_WFvS06W5Z8SBfsNZSgL9hxtSsW25HXs2SpSHcxJhCy'
# app.config['MYSQL_DATABASE_DB'] = 'foodapp'
# app.config['MYSQL_DATABASE_HOST'] = 'aws.connect.psdb.cloud'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ujrghqg0ika5puwyz8fp:pscale_pw_WFvS06W5Z8SBfsNZSgL9hxtSsW25HXs2SpSHcxJhCy@aws.connect.psdb.cloud/foodapp'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine("mysql://root:amrutha@localhost/zomato", echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:amrutha@localhost/zomato'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your models
import models

# Create MySQL object
mysql = MySQL(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# API endpoints

# Get menu items
@app.route('/menu', methods=['GET'])
def get_menu():
    menu_items = models.Menu.query.all()
    menu_list = []
    for item in menu_items:
        menu_dict = {
            'dish_id': item.dish_id,
            'dish_name': item.dish_name,
            'image_link': item.image_link,
            'dish_price': item.dish_price,
            'availability': item.availability
        }
        menu_list.append(menu_dict)
    return jsonify(menu_list)

# Add an item to the menu
@app.route('/menu', methods=['POST'])
def add_to_menu():
    data = request.get_json()
    dish_id = data.get('dish_id')
    dish_name = data.get('dish_name')
    image_link = data.get('image_link')
    dish_price = data.get('dish_price')
    availability = data.get('availability', True)

    menu_item = models.Menu(
        dish_id=dish_id,
        dish_name=dish_name,
        image_link=image_link,
        dish_price=dish_price,
        availability=availability
    )
    db.session.add(menu_item)
    db.session.commit()

    return jsonify({'message': 'Item added to the menu successfully'})

# Update a menu item
@app.route('/menu/<dish_id>', methods=['PUT'])
def update_menu_item(dish_id):
    menu_item = models.Menu.query.filter_by(dish_id=dish_id).first()
    if menu_item:
        data = request.get_json()
        menu_item.dish_name = data.get('dish_name', menu_item.dish_name)
        menu_item.image_link = data.get('image_link', menu_item.image_link)
        menu_item.dish_price = data.get('dish_price', menu_item.dish_price)
        menu_item.availability = data.get('availability', menu_item.availability)
        db.session.commit()
        return jsonify({'message': 'Menu item updated successfully'})
    else:
        return jsonify({'error': 'Menu item not found'}), 404

# Delete a menu item
@app.route('/menu/<dish_id>', methods=['DELETE'])
def delete_menu_item(dish_id):
    menu_item = models.Menu.query.filter_by(dish_id=dish_id).first()
    if menu_item:
        db.session.delete(menu_item)
        db.session.commit()
        return jsonify({'message': 'Menu item deleted successfully'})
    else:
        return jsonify({'error': 'Menu item not found'}), 404

# Add an order
@app.route('/order', methods=['POST'])
def add_order():
    data = request.get_json()
    user_id = data.get('user_id')
    dishes = data.get('dishes')
    total_price = data.get('total_price')
    status = data.get('status', 'pending')

    order = models.Order(
        user_id=user_id,
        dishes=dishes,
        total_price=total_price,
        status=status
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order added successfully'})

# Update order status
@app.route('/order/<order_id>', methods=['PUT'])
def update_order_status(order_id):
    order = models.Order.query.filter_by(id=order_id).first()
    if order:
        data = request.get_json()
        order.status = data.get('status', order.status)
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'})
    else:
        return jsonify({'error': 'Order not found'}), 404

# Cancel an order
@app.route('/order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    order = models.Order.query.filter_by(id=order_id).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order canceled successfully'})
    else:
        return jsonify({'error': 'Order not found'}), 404

# Register a new user
@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    user = models.User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

# User login
@app.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')

    user = models.User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'User not found'}), 404

# Add more endpoints for admin functionalities

if __name__ == '__main__':
    app.run(debug=True)