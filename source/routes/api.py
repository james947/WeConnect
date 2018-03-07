from flask import Flask, jsonify, abort, request
from source.models.business import Business
from source.models.users import User
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY']="b'409ce0cacf23b39b71faccfcb2f9fc3051c587d6155efa77'"
"""
Enables use of token

"""

user_instance = User()
# def add_user(username,email,password,public_id):
#     new_user=dict(username=username,email=email,password=password,public_id=public_id)
#     USERS.append(new_user)
    
@app.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user=request.get_json()
    email = user['email']
    username = user['username']
    password= user['password']

    if not email or not username or not password:
        return jsonify({'message':'Invalid input, please try again!'})

    password=sha256_crypt.encrypt(str(password))
    print (password)
    user_instance.create_user(id, username, email, password)
    print(user_instance.users)
    return jsonify({'Message':'User successfully registered'}),201

@app.route('/api/auth/login', methods = ['POST'])
def login():
    user=request.get_json()
    username = user['username']
    password =user['password']
    for user in user_instance.users:
       if user.username['username'] == "" or  user.password['password'] == "":
            return jsonify({'message': 'Username / password ivalid, please try again!'})
    return jsonify({'message':'logged in successfully'}),201
            


@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    return jsonify({"users": user_instance.users}), 200

@app.route('/api/v1/business', methods=['POST'])
def register_business():
    new_business = request.get_json()
    business = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']

    if not business or not description or not category or not location:
         return jsonify({'message':'Invalid input, please try again!'})


    
