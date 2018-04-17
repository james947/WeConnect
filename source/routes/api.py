from flask import Flask, jsonify, abort, request, make_response, json, session
from source.models.business import Business
from source.models.users import User
from source.models.reviews import Reviews
from passlib.hash import sha256_crypt
import datetime
import re

app = Flask(__name__)
"""secret key for encoding ofthe token"""
app.config['SECRET_KEY'] ="b'd45871881ac4561fb7bf9226e27137708e28c505fc21efb9'"
"""returns onbject as a dict making json serializable"""

BUSINESS = []
USERS = []
REVIEWS = []
    
@app.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user = request.get_json()
    email = user['email']
    username = user['username']
    password = user['password']
    available_emails = [x.email for x in USERS]
   
    if email in available_emails:
        return make_response(jsonify({'message':'Email is already registered'}),400)
    elif username == "":
        return make_response(jsonify({'message':'Username is required'}),401)
    elif email == "":
        return make_response(jsonify({'message':'Email is required'}),401)
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return jsonify({'message':'Email is invalid'})

    elif password == "":
        return make_response(jsonify({'message':'Password is required'}))
        
    password=sha256_crypt.encrypt(str(password))
    new_user=User(username, email, password)
    USERS.append(new_user)
    return make_response(jsonify({'message':'User successfully registered'}),201)

@app.route('/api/v1/login', methods = ['POST'])
def login():
    """if request is validated then user is logged in."""
    user_request = request.get_json()
    session.pop('current_user', None)
    email = user_request['email']
    password = user_request['password']

    if email== "":
        return make_response(jsonify({'message':'Email is required'}))
    elif password == "":
        return make_response(jsonify({'message':'Password is required'}))   
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return make_response(jsonify({'message':'Email is invalid'}))
    """Checcks for user by email"""
    user_login = [user for user in USERS if user.email == email]
    if user_login:
        user_login = user_login[0]
        is_user_password = sha256_crypt.verify(str(password), user_login.password)
        if is_user_password and email == user_login.email:
            session["current_user"] = user_login.email
            return jsonify({'message':'logged in successfully'}), 200
        return jsonify({'message':'Password not correct'})
    return make_response(jsonify({'message':'Email not found'}))


@app.route('/api/v1/auth/logout')
def logout():
    """clears sessions"""
    session.pop('current_user', None)
    return jsonify({'message':'Logged out successfuly'})

@app.route('/api/v1/auth/reset-password', methods = ['PUT'])
def reset_password():
    """Resets password"""
    reset = request.get_json()
    email = reset['email']
    new_password = reset['password']

    available_users =[user.email for user in USERS]
    if email not in available_users:
        return make_response(jsonify({'message':'Email not found'}))
    elif email == "":
        return make_response(jsonify({'message':'Email is required'}))
    elif new_password == "":
        return make_response(jsonify({'message':'Password is required'}))   
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return make_response(jsonify({'message':'Email is invalid'}))
    #confirm password
    get_user = [user for user in USERS if user.email == email]
    found_user = get_user[0]
    found_user.password = new_password
    return jsonify({'message':'Password reset success'})


@app.route('/api/v1/auth/users', methods=['GET'])
def get_all_users():
    """returns all the registered users"""
    # found_user=[{user.id : [user.email,user.username,user.password ] for user in USERS}]
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
    print(new_business)
    businessname = new_business['businessname']
    description = new_business['description']
    category = new_business['category']
    location = new_business['location']
    available_business = [biz.businessname for biz in BUSINESS]
    #test user in session
    if businessname in available_business:
        return jsonify({'message': 'Business already exists'}), 409
    elif businessname == "":
        return jsonify({'message': 'Business name required'}), 400
    elif description == "":
        return jsonify({'message': 'Description is  required'}), 400
    elif category == "":
        return jsonify({'message': 'Category is required'}), 400
    elif location == "":
        return jsonify({'message': 'Location is required'}), 400
 
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
        return jsonify({'message':'Business not found'}),404
    found_business = {
                    'id':business.id,
                    'businessname':business.businessname,
                    'description':business.description,
                    'category':business.category,
                    'location':business.location
                   }
    return make_response(jsonify(found_business),200)

@app.route('/api/v1/business/<int:business_id>', methods=['PUT'])
def update_by_id(business_id):
    """"updates business by id"""
    #get business by id then update from the json post request
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
        if business in BUSINESS:
            return jsonify({'message':'Business already exists'}),409

    business.businessname= request.json['businessname']
    business.description= request.json['description']
    business.category= request.json['category']
    business.location= request.json['location']
    business = BUSINESS
    updated_business=[{business.id : [{'businessname':business.businessname,'description':business.description,'category':business.category,
                                        'location':business.location}] for business in BUSINESS}]
    return make_response(jsonify(updated_business),200)


@app.route('/api/v1/business/<int:business_id>', methods=['DELETE'])
def delete_business_by_id(business_id):
    """Endpoint for deleting requested business by id"""
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
    BUSINESS.remove(business)
    return jsonify({'message':'Business successfully deleted'}),202


@app.route('/api/v1/business/<int:business_id>/review', methods=['POST'])
def add_review(business_id):
    new_review = request.get_json()
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]

    title = new_review['title'],
    description = new_review['description']
    business_id = business.id

    if title == "":
        return make_response(jsonify({'message':'Title is required'}), 401)
    elif description == "":
        return make_response(jsonify({'message':'Description is  required'}), 401)

    new_review =Reviews(title,description,business_id)
    REVIEWS.append(new_review)
    return make_response(jsonify({'message':'Review Added Successfully'}),201)



@app.route('/api/v1/business/<int:business_id>/review', methods=['GET'])
def get_all_reviews(business_id):
    business = [business for business in BUSINESS if business.id == business_id]
    if business:
        business = business[0]
    else:
        return jsonify({'message': 'Reviews not found'})

    business_id = business.id
    reviews = [review for review in REVIEWS if review.business_id == business_id]
    found_business = [{review.id: {'title': review.title, 'description': review.description}} for review in reviews]
    return make_response(jsonify(found_business), 200)
    
 