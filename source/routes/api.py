from flask import Flask, jsonify, abort, request, make_response
from source.models.business import Business
from source.models.users import User
from passlib.hash import sha256_crypt
import datetime
import re

app = Flask(__name__)

USERS = []
    
@app.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user=request.get_json()
    email = user['email']
    username = user['username']
    password= user['password']
    available_emails = [x.email for x in USERS]
   
    if email in available_emails:
        return make_response(jsonify({'message':'Email is already registered'}),400)
    elif username == "":
        return make_response(jsonify({'message':'Username is required'}),401)
    elif email== "":
        return make_response(jsonify({'message':'Email is required'}))
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return jsonify({'message':'Email is invalid'})

    elif password == "":
        return make_response(jsonify({'message':'Password is required'})
)
    password=sha256_crypt.encrypt(str(password))
    new_user=User(username, email, password)
    USERS.append(new_user)
    return make_response(jsonify({'Message':'User successfully registered'}),201)

@app.route('/api/v1/login', methods = ['POST'])
def login():
    """if request is validated then user is logged in."""
    user_request=request.get_json()
    email = user_request['email']
    password = user_request['password']
    user_login = [user for user in USERS if user.email == email]

    available_users=[user.email for user in USERS]
    if email not in available_users:
        return make_response(jsonify({'message':'Email not found'}))
    elif email== "":
        return make_response(jsonify({'message':'Email is required'}))
    elif password == "":
        return make_response(jsonify({'message':'Password is required'}))   
    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return make_response(jsonify({'message':'Email is invalid'}))
    if user_login:
        if password == user_login[0].password:
            return make_response(jsonify({'message':'logged in successfully'}), 200)


@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    """returns all the registered users"""
    #found_users=[{user.id : [user.email,user.username,user.password ] for user in USERS}]
    # user=[user.user for user in USERS}
    # [{x.id : [x.name, x.category, x.location] for x in businesses}]
    found_user = {
                  'id': user.id,
                  'email'  user.email,
                   'password': user.password,
                   'username':user.username] 
                    }

    return jsonify(found_user)


@app.route('/api/v1/business', methods=['POST'])
def register_business():
    """Registers non existing businesses"""
    new_business = request.get_json()
    if  new_business=="":
        return jsonify({'message':'error'})
    businessname = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']

    if businessname == "":
        return jsonify({'message':'Business name required'})
    elif description == "":
        return jsonify({'messaage':'Description is not required'})
    elif category == "":
        return jsonify({'message':'Category required'})
    elif location == "":
        return jsonify ({'message':'Location required'})
 
    for busines in business_instance.business:
        if busines['businessname'] ==businessname:
            return jsonify({'message':'Business already exists'}),409

    business_instance.create_business(id,businessname,description,location,category)
    #print(business_instance.create_business(id,businessname,description,location,category))
    return jsonify({'Message':'Business successfully registered'}),201

@app.route('/api/v1/business/', methods= ['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""
    for business in business_instance.business:
        if business['id'] == 0:    
            return  jsonify({'message':'businesses not found'}),404

        print(business_instance.business)
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


@app.route('/api/v1/business/<int:business_id>/', methods=['DELETE'])
def delete_business_by_id(business_id):
    """Endpoint for deleting requested business by id"""
    business=[business for business in business_instance.business if business['id']==business_id]
    business_instance.business.remove(business[0])
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
    if location == type(int):
        return jsonify({'message':'Invalid location'})
    business=[business for business in business_instance.business if business['location']==location]
    found_location ={
                    'id':business[0]['id'],
                    'businessname':business[0]['businessname'],
                    'description':business[0]['description'],
                    'category':business[0]['category'],
                    'location':business[0]['location']
                    }
    return jsonify(found_location),200







    
