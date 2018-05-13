from flask import Flask, jsonify, request, json, session
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_raw_jwt
)
from passlib.hash import sha256_crypt

from api.models.business import Business
from api.models.users import User
from api.models.reviews import Reviews
from api.api import validate


app = Flask(__name__)
"""secret key for encoding ofthe token"""
app.config['SECRET_KEY'] = "b'd45871881ac4561fb7bf9226e27137708e28c505fc21efb9'"

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)


BUSINESS = []
USERS = []
REVIEWS = []


blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.route('/api/v1/auth/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user = request.get_json()
    email = user.get('email')
    username = user.get('username')
    password = user.get('password')
    available_emails = [x.email for x in USERS]
    dict_data = {'Email': email, 'Username':username, 'Password':password}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
    if validate.email(email):   
        return jsonify(validate.email(email)), 401    
    if email in available_emails:
        return jsonify({'message': 'Email is already registered'}), 409
    if validate.key_password(password):
        return jsonify(validate.key_password(password))
    if validate.key_username(username):
        return jsonify(validate.key_username(username))

    password = sha256_crypt.encrypt(str(password))
    new_user = User(username, email, password)
    print(new_user)
    USERS.append(new_user)
    return jsonify({'message': 'User successfully registered'}), 201

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """if request is validated then user is logged in."""
    user_request = request.get_json()
    email = user_request.get('email')
    password = user_request.get('password')
    dict_data = {'Email': email, 'Password':password}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
    if validate.email(email):   
        return jsonify(validate.email(email)), 401   
    """Checks for user by email"""
    user_login = [user for user in USERS if user.email == email]
    if user_login:
        user_login = user_login[0]
        is_user_password = sha256_crypt.verify(str(password), user_login.password)
        if is_user_password and email == user_login.email:
            access_token = create_access_token(identity=email)
            response = {'token': access_token}
            return jsonify(response), 201
        return jsonify({'message': 'Password not correct'}), 403
    return jsonify({'message': 'Email not found'}), 404


@app.route('/api/v1/auth/logout', methods=["DELETE"])
@jwt_required
def logout():
    dumps = get_raw_jwt()['jti']
    blacklist.add(dumps)
    return jsonify({"msg": "Successfully logged out"}), 200   

@app.route('/api/v1/auth/reset-password', methods=['PUT'])
@jwt_required
def reset_password():
    """Resets password"""
    reset = request.get_json()
    email = reset.get(email)
    current_password = reset.get('current_password')
    new_password = reset.get('new_password')
    dict_data = {'current_password': current_password, 'new_password': new_password}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
    # confirm password
    get_user = [user for user in USERS if user.password == dict_data.get('password') 
    and user.email == dict_data.get('email')]
    print(get_user)
    if get_user:
        get_user.password = new_password
        return jsonify({'message': 'Password reset success'}), 200
    return jsonify({'message': 'username or password is invalid'}), 401


@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """returns all the registered users"""
    result = []
    for user in USERS:      
        found_user = {
            'user_id': user.id,
            'email': user.email,
            'user_name': user.username
            }
        result.append(found_user)
    return jsonify(result)


@app.route('/api/v1/business', methods=['POST'])
@jwt_required
def register_business():
    """Registers non existing businesses"""
    new_business = request.get_json()
    businessname = new_business.get('businessname')
    description = new_business.get('description')
    category = new_business.get('category')
    location = new_business.get('location')
    dict_data = {'Businessname': businessname, 'Description': description,
    'Category': category, 'Location': location}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401

    available_business = [biz.businessname for biz in BUSINESS]

    if businessname in available_business:
        return jsonify({'message': 'Business already exists'}), 409
 
    new_business = Business(businessname, description, location, category)
    BUSINESS.append(new_business)
    return jsonify({'message': 'Business successfully registered'}), 201

@app.route('/api/v1/business/', methods=['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""
    get_business = [business for business in BUSINESS]
    if not get_business:
            return jsonify({'message':'Business not found'}), 409
    found_business = [{'businessname': business.businessname, 'description': business.description,
    'category': business.category, 'location': business.location, 'id': business.id } for business in BUSINESS]
    return jsonify(found_business), 200

@app.route('/api/v1/business/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular bsuiness by id"""
    business = [business for business in BUSINESS if business.id == business_id]
    if business:
        business = business[0]
    elif business not in BUSINESS: 
        return jsonify({'message': 'Business not found'}), 404
    found_business = {
                    'id': business.id,
                    'businessname': business.businessname,
                    'description': business.description,
                    'category': business.category,
                    'location': business.location
                   }
    return jsonify(found_business), 200


@app.route('/api/v1/business/<int:business_id>', methods=['PUT'])
@jwt_required
def update_by_id(business_id):
    """"updates business by id"""
    dict_data = request.get_json()

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 4011

    businessname = dict_data.get('businessname')
    business_names = [business.businessname for business in BUSINESS]
    if businessname in business_names:
        return jsonify({'message': 'Business already exists'}), 409

    target_business = None
    for business in BUSINESS:
        if business.id == business_id:
            target_business = business
            break
    if not target_business:
        return jsonify({"message": "Business not found"})   
    for key in dict_data.keys():
        value = dict_data[key]
        setattr(target_business, key, value)

    updated_business = {'business.id': target_business.id, 'businessname': target_business.businessname,
    'description': target_business.description, 'category': target_business.category,
    'location': target_business.location} 
    return jsonify(updated_business), 200   

@app.route('/api/v1/business/<int:business_id>', methods=['DELETE'])
@jwt_required
def delete_business_by_id(business_id):
    """Endpoint for deleting requested business by id"""
    target_business = None
    for business in BUSINESS:
        if business.id == business_id:
            target_business = business

    if target_business:
        BUSINESS.remove(target_business)
        return jsonify({'message': 'Business successfully deleted'}), 202
    return jsonify({'message': 'Business not found'}), 404

@app.route('/api/v1/business/<int:business_id>/review', methods=['POST'])
def add_review(business_id):
    new_review = request.get_json()
    title = new_review.get('title')
    description = new_review.get('description')
    dict_data = {'Title': title, 'Description': description}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
        
    business = [business for business in BUSINESS if business.id == business_id]
    if business:
        business = business[0] 
        business_id = business.id
        new_review = Reviews(title, description, business_id)
        REVIEWS.append(new_review)
        return jsonify({'message': 'Review Added Successfully'}), 201
    return jsonify({'message': 'Business not found'}), 404

@app.route('/api/v1/business/<int:business_id>/review', methods=['GET'])
def get_all_reviews(business_id):
    business = [business for business in BUSINESS if business.id == business_id]
    if business:
        business = business[0]
        business_id = business.id
        review = [{'title': review.title, 'description': review.description} for review in REVIEWS]
        return jsonify(review), 200
    return jsonify({'message': 'Reviews not found'}), 404

    
 