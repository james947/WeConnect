from flask import jsonify, request, make_response, session, Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from api import mail
from flask_mail import Message


from api.base_model import db
from api.users.models import Users, Blacklist
from api.helpers.token import token_required
from api.helpers import validate
from api import create_app


auth = Blueprint('auth', __name__)


@auth.route('/api/v1/auth/register', methods=['POST'])
def create_user():
    """creates a new user in the list of users"""
    dict_data = request.get_json()
    try:
        data = validate.validator(dict_data)
    except AssertionError as error:
        return jsonify({"message": error.args[0]})
    available_emails = Users.query.filter_by(email=data['email']).first()
    if available_emails == None:
        """checks if email duplicate email"""
        password = generate_password_hash(
            data.get('password'), method='sha256')
        new_user = Users(public_id=str(uuid.uuid4()), username=data.get(
            'username'), email=data.get('email'), password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'Message': 'User successfully registered'}), 201
    elif dict_data.get('email') in available_emails.email:
        return jsonify({'message': 'Email is already registered'}), 400


@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    """if request is validated then user is logged in."""
    dict_data = request.get_json()

    try:
        data = validate.login_validator(dict_data)

    except AssertionError as error:
        return jsonify({"message": error.args[0]})

    """seach user in db"""
    user = Users.query.filter_by(email=dict_data.get('email')).first()

    if not user:
        return jsonify({'message': 'Email not found please try again'}), 404
    """checks correct password"""
    if check_password_hash(user.password, data.get('password')):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=1)}, os.getenv('SECRET'))
        return jsonify({'token': token.decode('UTF-8')})
    return jsonify({'message': 'Wrong Password'}), 401


@auth.route('/api/v1/auth/logout', methods=['DELETE'])
@token_required
def logout(current_user=None):
    """clears sessions"""
    token = request.headers.get('x-access-token')
    blacklist = Blacklist(token)
    blacklist.save()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth.route('/api/v1/auth/change-password', methods=['PUT'])
@token_required
def change_password(current_user):
    """Resets password"""
    dict_data = request.get_json()

    available_users = Users.query.filter_by(
        email=dict_data.get('email')).first()

    if not available_users:
        return jsonify({'message': 'Email not found'})

    if current_user.id == available_users.owner_id:
        try:
            data = validate.reset_validator(dict_data)
        except AssertionError as error:
            return jsonify({"message": error.args[0]})

        current_user.password = data.get('password')
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'message': 'Password reset success'}), 200


@auth.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    """Resets password"""
    dict_data = request.get_json()

    email = dict_data.get('email')

    get_email = Users.query.filter_by(email=email).first()
    if get_email:
        password = str(uuid.uuid4())[:8]
        get_email.password = generate_password_hash(password, method='sha256')
        db.session.commit()

        message = Message(
            subject="Password Reset",
            sender='hcravens25@gmail.com',
            recipients=[get_email.email],
            body="Hello" + get_email.username + ",\n Your new password is:" + password
        )
        mail.send(message)
        return jsonify({'message': 'An email has been sent with your new password!'}), 200

    return jsonify({'message': 'Non-existent email. Try signing up'}), 404
