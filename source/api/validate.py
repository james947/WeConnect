'''Validations'''
import re


def blank(**data):
    for key in data:
        name = re.sub(r'\s+', '', data[key])
        if not name:
            return {'message': key + ' is required'}


def email(data):
    vemail = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data)
    if not vemail:
        return {'message': 'Email is invalid'}


def key_blank(**data):
    for key in data:
        if data[key] is None:
            return {'message': key + ' is missing'}


def key_username(username):
    match = re.match(r'^[a-zA-Z_]+[\d\w]{3,}', username)
    if match is None:
        return {'message': 'Username should contain atleast (a-z), (0-4), (-), (_), characters(4)'} 


def key_password(password):
    password = re.match(r'[a-zA-Z_]+[\d\w]{8,}', password)
    if password is None:
        return {'message': 'password should contain atleast (a-z), (0-4), (-), characters(8)'}