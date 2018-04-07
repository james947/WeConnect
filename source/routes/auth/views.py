from . import auth
from flask import Flask, jsonify, abort, request, make_response, json, session, Blueprint
from functools import wraps
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

from source.models.models import Users, db



def token_required(f):
    """Decorator to secure all endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
  
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is required'}), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET'))
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated





@auth.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user=request.get_json()
    email = user['email']
    username = user['username']
    password= user['password']

    # if username.strip():
    #     return make_response(jsonify({'message':'Whitespaces are not allowed'}),401)
    if username == "":
        return make_response(jsonify({'message':'Username is required'}),401)
    elif email== "":
        return make_response(jsonify({'message':'Email is required'}))
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return make_response(jsonify({'message':'Email is invalid'}))
    elif password == "":
        return make_response(jsonify({'message':'Password is required'}),401)

    available_emails =  Users.query.filter_by(email=email).first()
    if available_emails == None:
        """checks if email duplicate email"""
        password=generate_password_hash(password, method='sha256')
        new_user=Users(public_id=str(uuid.uuid4()), username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'Message':'User successfully registered'}),201)
    elif email in available_emails.email:
        return make_response(jsonify({'message':'Email is already registered'}),400) 

        

@auth.route('/api/v1/login', methods = ['POST'])
def login():
    """if request is validated then user is logged in."""
    user_request=request.get_json()
    session.pop('user', None)
    username = user_request['username']
    password = user_request['password']

    if username== "":
        return make_response(jsonify({'message':'Username is required'}),401)
    elif password == "":
        return make_response(jsonify({'message':'Password is required'}),401)   
    """seach user in db"""
    user =  Users.query.filter_by(username=username).first()
    if not user:
        return make_response(jsonify({'message':'User not found'}))
    """checks correct password"""
    if check_password_hash(user.password, password):
        session['loggedin'] = True
        session['username'] = user_request['username']
        token =jwt.encode({'public_id' : user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes =25)}, os.getenv('SECRET'))
        return jsonify({'token':token.decode('UTF-8')})
    return make_response(jsonify({'message':'Wrong Password'}))

@auth.route('/api/auth/logout', methods=['DELETE'])
def logout():
    """clears sessions"""
    if session and session['loggedin']:
        session.clear()
    return make_response(jsonify({'message':'Logged out successfully'}), 200)
    
@auth.route('/api/v1/auth/reset-password', methods = ['PUT'])
@token_required
def reset_password(current_user):
    """Resets password"""
    reset = request.get_json()
    email= reset['email']
    new_password = reset['password']
    
    available_users= Users.query.filter_by(email=email).first()
    if not available_users:
        return make_response(jsonify({'message':'Email not found'}))
    elif email== "":
        return make_response(jsonify({'message':'Email is required'}),401)
    elif new_password == "":
        return make_response(jsonify({'message':'Password is required'}),401)   
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return make_response(jsonify({'message':'Email is invalid'}))

    current_user.password = new_password
    db.session.add(current_user)
    db.session.commit()
    return make_response(jsonify({'message':'Password reset success'}),200)

@auth.route('/api/auth/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    """returns all the registered users"""
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)

    return make_response(jsonify({'users':output}),200)

