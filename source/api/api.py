from flask import Flask, jsonify, abort, request, make_response, json, session
from source.models.business import Business
from source.models.users import User
from source.models.reviews import Reviews
from passlib.hash import sha256_crypt
from source.routes import validate
import datetime
import re
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)



app = Flask(__name__)
"""secret key for encoding ofthe token"""
app.config['SECRET_KEY'] ="b'd45871881ac4561fb7bf9226e27137708e28c505fc21efb9'"

jwt = JWTManager(app)

BUSINESS = []
USERS = []
REVIEWS = []
    
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
        return jsonify({'message':'Email is already registered'}), 400

    password=sha256_crypt.encrypt(str(password))
    new_user=User(username, email, password)
    USERS.append(new_user)
    return jsonify({'message':'User successfully registered'}), 201

@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    """if request is validated then user is logged in."""
    user_request = request.get_json()
    session.pop('current_user', None)
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
            return jsonify(access_token), 200
        return jsonify({'message':'Password not correct'})
    return jsonify({'message':'Email not found'}), 401


@app.route('/api/v1/auth/logout' ,methods=["DELETE"])
def logout():
    """clears sessions"""
    session.pop('current_user', None)
    return jsonify({'message':'Logged out successfuly'})

@app.route('/api/v1/auth/reset-password', methods = ['PUT'])
def reset_password():
    """Resets password"""
    reset = request.get_json()
    current_password = reset.get('current_paswword')
    new_password = reset.get('new_password')
    dict_data = {'current_password': current_password, 'new_password':new_password}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
    #confirm password
    get_user = [user for user in USERS if user.password == current_password]
    found_user = get_user[0]
    found_user.password = new_password
    return jsonify({'message':'Password reset success'})


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
def register_business():
    """Registers non existing businesses"""
    new_business = request.get_json()
    businessname = new_business.get('businessname')
    description = new_business.get('description')
    category = new_business.get('category')
    location = new_business.get('location')
    dict_data = {'Businessname': businessname, 'Description':description, 
    'Category':category, 'Location':location}

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
    business = BUSINESS
    found_business =[{'businessname': business.businessname, 'description':business.description,
    'category': business.category,'location':business.location ,'id':business.id } for business in BUSINESS]
    return jsonify(found_business),200                

@app.route('/api/v1/business/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular bsuiness by id"""
    business =[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
    elif business not in BUSINESS: 
        return jsonify({'message':'Business not found'}), 404
    found_business = {
                    'id':business.id,
                    'businessname':business.businessname,
                    'description':business.description,
                    'category':business.category,
                    'location':business.location
                   }
    return jsonify(found_business), 200

@app.route('/api/v1/business/<int:business_id>', methods=['PUT'])
def update_by_id(business_id):
    """"updates business by id"""
    new_update = request.get_json()
    businessname = new_update.get('businessname')
    description = new_update.get('description')
    category = new_update.get('category')
    location = new_update.get('location')

    dict_data = {'Businessname': businessname, 'Description':description, 
    'Category':category, 'Location':location}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401

    available_business = [biz.businessname for biz in BUSINESS]
    business = available_business[0]
    if businessname in business:
        return jsonify({'message': 'Business already exists'}), 409
    business.businessname = businessname
    print(businessname)
    business.description = description
    business.category = category
    business.location = location
    updated_business=[{'business.id' :business.id, 'businessname':business.businessname,
    'description':business.description,'category':business.category,
    'location':business.location} for business in BUSINESS]
    return jsonify(updated_business), 200   

@app.route('/api/v1/business/<int:business_id>', methods=['DELETE'])
def delete_business_by_id(business_id):
    """Endpoint for deleting requested business by id"""
    target_business= None
    for business in BUSINESS:
        if business.id==business_id:
            target_business = business
    
    if target_business:
        BUSINESS.remove(target_business)
        return jsonify({'message':'Business successfully deleted'}), 202
    return jsonify({'message':'Business not found'}), 404

@app.route('/api/v1/business/<int:business_id>/review', methods=['POST'])
def add_review(business_id):
    new_review = request.get_json()
    title = new_review.get('title')
    description = new_review.get('description')
    dict_data = {'Title': title, 'Description':description}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
        
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0] 
        business_id = business.id
        new_review =Reviews(title,description,business_id)
        REVIEWS.append(new_review)
        return jsonify({'message':'Review Added Successfully'}), 201
    return jsonify({'message':'Business not found'}), 404

@app.route('/api/v1/business/<int:business_id>/review', methods=['GET'])
def get_all_reviews(business_id):
    business = [business for business in BUSINESS if business.id == business_id]
    if business:
        business = business[0]
        business_id = business.id
        review = [{'title':review.title, 'description':review.description} for review in REVIEWS]
        return jsonify(review), 200
    return jsonify({'message': 'Reviews not found'}), 404

    
 