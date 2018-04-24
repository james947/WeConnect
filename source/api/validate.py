'''Validations'''
import re


def blank(**data):
    for key in data:
        name = re.sub(r'\s+','',data[key])
        if not name:

            return {'message':key + ' is required'}
def email(data):
    vemail = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",data)
    if not vemail:
        return {'message':'Email is invalid'}


def key_blank(**data):
    for key in data:
        if data[key] is None:
            return {'message': key + ' is Missing'}


def key_username(**data):
    for key in data:
        username = re.match(r'^[a-zA-Z_]+[\d\w]{4,}', data[key])
        if not username:
            return {'message': key + ' should contain atleast (a-z), (0-4), (-), (_), characters(4)'}


def key_password(**data):
    for key in data:
        password = re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', data[key])
        if not password:
            return {'message': key + ' should contain atleast (a-z), (0-4), (-), (_), characters(8)'}