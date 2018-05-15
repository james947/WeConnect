from functools import wraps
import jwt
import os
from api.users.models import Users
from flask import Flask, jsonify, abort, request, make_response, json, session, Blueprint

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