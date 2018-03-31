from . import auth
from flask import Flask, jsonify, abort, request, make_response,json, session,Blueprint
from functools import wraps
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os


from source.models.models import Users


@auth.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user=request.get_json()
    email = user['email']
    username = user['username']
    password= user['password']
    
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
    # session.pop('user', None)
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
        # session['username'] = user_request['username']
        token =jwt.encode({'public_id' : user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes =25)}, os.getenv('SECRET'))
        return jsonify({'token':token.decode('UTF-8')})
    return make_response(jsonify({'message':'Wrong Password'}))

@auth.route('/api/auth/logout')
def logout():
    """clears sessions"""
    session.pop('user', None)
    return make_response(jsonify({'message':'Logged out successfuly'}), 200)
    
@auth.route('/api/v1/auth/reset-password', methods = ['PUT'])
def reset_password():
    """Resets password"""
    reset = request.get_json()
    email= reset['email']
    new_password = reset['password']

    available_users=[user.email for user in USERS]
    if email not in available_users:
        return make_response(jsonify({'message':'Email not found'}))
    elif email== "":
        return make_response(jsonify({'message':'Email is required'}),401)
    elif new_password == "":
        return make_response(jsonify({'message':'Password is required'}),401)   
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return make_response(jsonify({'message':'Email is invalid'}))

    get_user = [user for user in USERS if user.email == email]
    found_user = get_user[0]
    found_user.password = new_password
    return make_response(jsonify({'message':'Password reset success'}),200)

@auth.route('/api/auth/users', methods=['GET'])
def get_all_users():
    """returns all the registered users"""
    user = USERS
    #found_user=[{user.id : [user.email,user.username,user.password ] for user in USERS}]
    result =json.dumps(user, indent=4, separators=(',', ': '), default=json_default_format)
    return make_response(jsonify({'result':result}),200)

