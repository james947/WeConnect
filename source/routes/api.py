from flask import Flask, jsonify, abort, request, make_response,json
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
def json_default_format(o):
    return o.__dict__

BUSINESS=[]
USERS = []
REVIEWS = []
    
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
        return make_response(jsonify({'message':'Password is required'}))
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
    user = USERS
    #found_user=[{user.id : [user.email,user.username,user.password ] for user in USERS}]
    result =json.dumps(user, indent=4, separators=(',', ': '), default=json_default_format)
    return jsonify({'result':result})


@app.route('/api/v1/business', methods=['POST'])
def register_business():
    """Registers non existing businesses"""
    new_business = request.get_json()
    businessname = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']
    available_business= [biz.businessname for biz in BUSINESS]

    if  businessname in  available_business:
        return jsonify({'message':'Business already exists'}),409
    elif businessname == "":
        return jsonify({'message':'Business name required'}), 401
    elif description == "":
        return jsonify({'messaage':'Description is  required'}), 401
    elif category == "":
        return jsonify({'message':'Category required'}), 401
    elif location == "":
        return jsonify ({'message':'Location required'}), 401
 

    new_business=Business(businessname,description,location,category)
    BUSINESS.append(new_business)
    return jsonify({'Message':'Business successfully registered'}),201

@app.route('/api/v1/business/', methods= ['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""
    business = BUSINESS
    found_business=[{business.id : [{'businessname':business.businessname,'description':business.description,'category':business.category,'location':business.location}] for business in BUSINESS}]
    return make_response(jsonify(found_business),200)                


@app.route('/api/v1/business/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular bsuiness by id"""
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
    elif business.id < 0: 
        return  make_response(jsonify({'message':'business not found'}),404)
    elif business.id != business.id:
        return  make_response(jsonify({'message':'business not found'}),404)
    found_business={
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

@app.route('/api/v1/business/category/<string:category>', methods=['GET'])
def get_business_by_category(category):
    """Endpoint for filter by category"""
    #cheks if category is not a string
    business=[business for business in BUSINESS if business['category']==category]
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



@app.route('/api/v1/business/<int:business_id>/review', methods=['POST'])
def add_review(business_id):
    new_review = request.get_json()
    title = new_review['title'],
    description = new_review['description']
    business_id = new_review['businessid']

    if title == "":
        return make_response(jsonify({'message':'Title name required'}), 401)
    elif description == "":
        return make_response(jsonify({'messaage':'Description is  required'}), 401)

    new_review =Reviews(title,description,business_id)
    REVIEWS.append(new_review)

    return make_response(jsonify({'message':'Review Added Successfully'}),201)



@app.route('/api/v1/business/<int:business_id>/review/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review=[review for review in REVIEWS if review.id==review_id]
    if review:
        review = review[0]
    found_business={
                    'id':review.id,
                    'businessname':review.businessname,
                    'description':review.description,
                    'category':review.category,
                    'location':review.location
                   }
    return make_response(jsonify(found_business),200)
    
