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

USERS=[]
# def add_user(username,email,password,public_id):
#     new_user=dict(username=username,email=email,password=password,public_id=public_id)
#     USERS.append(new_user)
    
@app.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    username=request.get_json('username')
    email = request.get_json('email')
    password=request.get_json('password')
    """
    retrieves data from request and stores in data variable
    """
    if username['username'] == "":
        return jsonify({'Message':'Username cannot be null'})
    elif password['password']=="":
        return jsonify({'Message':'Password cannot be null'})
    elif email['email']=="":
        return jsonify({'Message':'email cannot be null'})


    new_user = User(public_id=str(uuid.uuid4()),username=username['username'],email=email['email'],password=sha256_crypt.encrypt(str(password['password'])))
    USERS.append(new_user)
    return jsonify({'Message':'User successfully registered'}),201

@app.route('/api/auth/login', methods = ['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"Message": "Authentication needed"}), 401
    
    for user in USERS:
        if auth.username == user['username'] and auth.password == user['password']:
            
            token = jwt.encode({'username': auth.username,  'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=25)}, app.config['SECRET_KEY'])
            
            return jsonify({"token": token.decode("UTF-8")}), 200
        return jsonify({'Message':'User not found'})


@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    return jsonify({"users": USERS}), 200

@app.route('/api/v1/business', methods=['POST'])
def register_business():
    new_business= Business()
