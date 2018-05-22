'''Validations'''
import re


def blank(data):
    for key in data:
        name = re.sub(r'\s+', '', data[key])
        if not name:
            assert 0, key + ' is required'


def emails(data):
    vemail = re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data)
    if not vemail:
        assert 0, 'Email is invalid'


def key_blank(data):
    for key in data:
        if data[key] is None:
            assert 0, key + ' is missing'


def key_username(username):
    match = re.match(r'^[a-zA-Z_]+[\d\w]{3,}', username)
    if match is None:
        assert 0, 'Username should contain atleast (a-z), (0-4), (-), (_), characters(4)'


def key_password(password):
    password = re.match(r'[a-zA-Z_\d\w]{8,}', password)
    if password is None:
        assert 0, 'password should contain atleast (a-z), (0-4), (-), characters(8)'


def validator(dict_data):
    """user data"""
    password = dict_data.get('password')
    username = dict_data.get('username')
    email = dict_data.get('email')

    dict_data = {'password': password, 'username': username, 'email': email}
    key_blank(dict_data)
    blank(dict_data)
    emails(email)
    key_password(password)
    key_username(username)

    return dict_data


def biz_validator(dict_data):
    """business data"""
    businessname = dict_data.get('businessname')
    description = dict_data.get('description')
    category = dict_data.get('category')
    location = dict_data.get('location')

    dict_data = {'businessname': businessname, 'description': description,
                 'category': category, 'location': location}

    key_blank(dict_data)
    blank(dict_data)

    return dict_data


def login_validator(dict_data):
    """user data"""
    password = dict_data.get('password')
    email = dict_data.get('email')

    dict_data = {'password': password, 'email': email}
    key_blank(dict_data)
    blank(dict_data)
    emails(email)
    key_password(password)

    return dict_data


def reset_validator(dict_data):
    """user data"""
    current_password = dict_data.get('current_password')
    new_password = dict_data.get('new_password')
    email = dict_data.get('email')

    dict_data = {'current_password': current_password,
                 'new_password': new_password, 'email': email}
    key_blank(dict_data)
    blank(dict_data)
    emails(email)
    key_password(current_password)
    key_password(new_password)

    return dict_data


def review_validator(dict_data):
    """user data"""
    title = dict_data.get('title')
    review = dict_data.get('review')

    dict_data = {'title': title, 'review': review}
    key_blank(dict_data)
    blank(dict_data)

    return dict_data