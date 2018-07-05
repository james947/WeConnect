from functools import wraps
import jwt
import os
from api.users.models import Users, Blacklist
from flask import Flask, jsonify, abort, request, make_response, json, session, Blueprint


def validate_token(token):
    is_error = False

    check_token = Blacklist.query.filter_by(token=token).first()
    if check_token:
        is_error = True
        return "Token Blacklisted", is_error

    try:
        payload = jwt.decode(token, os.getenv('SECRET'))
        return "Valid token", is_error
    except jwt.ExpiredSignatureError:
        is_error = True
        return 'Token expired. Please log in again', is_error
    except (jwt.InvalidTokenError, jwt.DecodeError):
        is_error = True
        return 'Invalid Token Please refresh', is_error


def token_required(f):
    """Decorator to secure all endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is required'}), 401

        message, is_error = validate_token(token)
        if is_error:
            return jsonify({"message": message}), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET'))
            current_user = Users.query.filter_by(
                public_id=data['public_id']).first()
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user=current_user, *args, **kwargs)

    return decorated
