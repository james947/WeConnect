'''Validations'''
import re

def blank(**data):
    for key in data:
        name = re.sub('r\s','',data[key])
        if not name:
            return {'message':key + ' is required'}
def email(data):
    vemail = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",data)
    if not vemail:
        return {'message':'Email is invalid'}

def key_blank(**data):
    for key in data:
        if data[key] is None:
            return {'message':key + ' is Missing'}