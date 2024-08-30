from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/userdb'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return 'Welcome to the User Management API'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    phone = data['phone']
    profession = data['profession']
    password = data['password']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    mongo.db.users.insert_one({
        'name': name,
        'email': email,
        'phone': phone,
        'profession': profession,
        'password': hashed_password
    })

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = mongo.db.users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/users', methods=['GET'])
def list_users():
    users = mongo.db.users.find()
    user_list = [{'name': user['name'], 'email': user['email'], 'phone': user['phone'], 'profession': user['profession']} for user in users]
    return jsonify(user_list)

@app.route('/update_user', methods=['PUT'])
def update_user():
    data = request.json
    email = data['email']
    new_name = data.get('name')
    new_phone = data.get('phone')

    update_data = {}
    if new_name:
        update_data['name'] = new_name
    if new_phone:
        update_data['phone'] = new_phone

    result = mongo.db.users.update_one({'email': email}, {'$set': update_data})

    if result.matched_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    email = data['email']

    result = mongo.db.users.delete_one({'email': email})

    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'})
