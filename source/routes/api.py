from flask import Flask, jsonify, abort, request
from source.models.business import Business
from source.models.users import User
from passlib.hash import sha256_crypt
import datetime
import re

app = Flask(__name__)


business_instance=Business()
user_instance = User()

    
@app.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user=request.get_json()
    email = user['email']
    username = user['username']
    password= user['password']

    for user in user_instance.users:
        if user['email'] == email:
            return jsonify({'message':'Email is already registered'})
    
    if username == "":
        return jsonify({'message':'Username is required'})
    
    elif email== "":
        return jsonify({'message':'Email is required'})
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return jsonify({'message':'Email is invalid'})

    elif password == "":
        return jsonify({'message':'Password is required'})

    password=sha256_crypt.encrypt(str(password))
    user_instance.create_user(id,username, email, password)
    return jsonify({'Message':'User successfully registered'}),201

@app.route('/api/v1/login', methods = ['POST'])
def login():
    """if request is validated then user is logged in."""
    user_request=request.get_json()
    for user in user_instance.users:
        if user['email'] ==user_request['email'] and user['password'] ==  user_request['password']:
            return jsonify({'message':'logged in successfully'}), 200
        elif user_request['email'] == "":
            return jsonify({'message':'Email is required'}),401
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",user_request['email']):
            return jsonify({'message':'Email is invalid'}),400
        elif user_request['password'] == "":
            return jsonify({'message':'Password is required'}),401
      

@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    """returns all the registered users"""
    return jsonify(user_instance.users), 200


@app.route('/api/v1/business', methods=['POST'])
def register_business():
    """Registers non existing businesses"""
    new_business = request.get_json()
    businessname = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']

    if businessname == "":
        return jsonify({'message':'Business name required'}), 401
    elif description == "":
        return jsonify({'messaage':'Description is  required'}), 401
    elif category == "":
        return jsonify({'message':'Category required'}), 401
    elif location == "":
        return jsonify ({'message':'Location required'}), 401
 
    for busines in business_instance.business:
        if busines['businessname'] ==businessname:
            return jsonify({'message':'Business already exists'}),409

    business_instance.create_business(id,businessname,description,location,category)
    #print(business_instance.create_business(id,businessname,description,location,category))
    return jsonify({'Message':'Business successfully registered'}),201

@app.route('/api/v1/business/', methods= ['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""
    return jsonify(business_instance.business),200                


@app.route('/api/v1/business/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular bsuiness by id"""
    busines=[business for business in business_instance.business if business['id']==business_id]
    if len(busines) < 0: 
        return  jsonify({'message':'business not found'}),404
    for business in business_instance.business:
        found_business={
                        'id':business['id'],
                        'businessname':business['businessname'],
                        'description':business['description'],
                        'category':business['category'],
                        'location':business['location']
                    }

    return jsonify(found_business),200

@app.route('/api/v1/business/<int:business_id>', methods=['PUT'])
def update_by_id(business_id):
    """"updates business by id"""
    #get business by id then update from the json post request
    busines=[business for business in business_instance.business if business['id']==business_id]

    busines[0]['businessname'] = request.json['businessname']
    busines[0]['description'] = request.json['description']
    busines[0]['category'] = request.json['category']
    busines[0]['location'] = request.json['location']
     
    return jsonify({'business':busines[0]}),200


@app.route('/api/v1/business/<int:business_id>', methods=['DELETE'])
def delete_business_by_id(business_id):
    """Endpoint for deleting requested business by id"""
    business=[business for business in business_instance.business if business['id']==business_id]
    del business_instance.business[0]['id']
    del business_instance.business[0]['businessname']
    del business_instance.business[0]['description']
    del business_instance.business[0]['category']
    del business_instance.business[0]['location']
    return jsonify({'message':'Business successfully deleted'}),202

@app.route('/api/v1/business/category/<string:category>', methods=['GET'])
def get_business_by_category(category):
    """Endpoint for filter by category"""
    #cheks if category is not a string
    business=[business for business in business_instance.business if business['category']==category]
    found_category ={
                    'id':business[0]['id'],
                    'businessname':business[0]['businessname'],
                    'description':business[0]['description'],
                    'category':business[0]['category'],
                    'location':business[0]['location']
                    }
    return jsonify(found_category),200


@app.route('/api/v1/business/location/<string:location>', methods=['GET'])
#"""Endpoint for filter by location"""
def get_business_by_location(location):
    #checks if location is not a string 
    if location == "":
        return jsonify({'message':'Invalid location'})
    for location in business_instance.business:
        if location not in business_instance.business:
            return jsonify({'messaage':'location not found'}), 401

    if location in business_instance.business:
        found_location ={
                        'id':location[0]['id'],
                        'businessname':location[0]['businessname'],
                        'description':location[0]['description'],
                        'category':location[0]['category'],
                        'location':location[0]['location']
                        }
    return jsonify(found_location), 200







    
