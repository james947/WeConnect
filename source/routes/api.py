from flask import Flask, jsonify, abort, request, make_response,json, session,Blueprint
from passlib.hash import sha256_crypt
from functools import wraps
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

biz = Blueprint('biz', __name__)
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config
 
# initialize sql-alchemy
db = SQLAlchemy()

"""wraps the creation of a new Flask object"""
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(biz)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .auth import auth
    app.register_blueprint(auth)
    return app

"""import model classes"""
from source.models.models import Users, Business, Reviews


@biz.route('/api/v1/business', methods=['POST'])
def register_business():
    """Registers non existing businesses"""
    new_business = request.get_json()
    businessname = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']
    available_business= [biz.businessname for biz in BUSINESS]

    if  businessname in  available_business:
        return make_response(jsonify({'message':'Business already exists'}),409)
    elif businessname == "":
        return jsonify({'message':'Business name required'}), 401
    elif description == "":
        return make_response(jsonify({'messaage':'Description is  required'}), 401)
    elif category == "":
        return make_response(jsonify({'message':'Category required'}), 401)
    elif location == "":
        return make_response(jsonify ({'message':'Location required'}), 401)
 
    new_business=Business(businessname,description,location,category)
    BUSINESS.append(new_business)
    return jsonify({'Message':'Business successfully registered'}),201

@biz.route('/api/v1/business/', methods= ['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""
    business = BUSINESS
    found_business=[{business.id : [{'businessname':business.businessname,'description':business.description,
    'category':business.category,'location':business.location}] for business in BUSINESS}]
    return make_response(jsonify(found_business),200)                


@biz.route('/api/v1/business/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular bsuiness by id"""
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
    elif business not in BUSINESS: 
        return  make_response(jsonify({'message':'business not found'}),404)
    found_business={
                    'id':business.id,
                    'businessname':business.businessname,
                    'description':business.description,
                    'category':business.category,
                    'location':business.location
                   }
    return make_response(jsonify(found_business),200)

@biz.route('/api/v1/business/<int:business_id>', methods=['PUT'])
def update_by_id(business_id):
    """"updates business by id"""
    #get business by id then update from the json post request
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
        if business in BUSINESS:
            return make_response(jsonify({'message':'Business already exists'}),409)

    business.businessname= request.json['businessname']
    business.description= request.json['description']
    business.category= request.json['category']
    business.location= request.json['location']
    business = BUSINESS
    updated_business=[{business.id : [{'businessname':business.businessname,'description':business.description,'category':business.category,
                                        'location':business.location}] for business in BUSINESS}]
    return make_response(jsonify(updated_business),200)


@biz.route('/api/v1/business/<int:business_id>', methods=['DELETE'])
def delete_business_by_id(business_id):
    """Endpoint for deleting requested business by id"""
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
    BUSINESS.remove(business)
    return jsonify({'message':'Business successfully deleted'}),202


@biz.route('/api/v1/business/<int:business_id>/review', methods=['POST'])
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
        return make_response(jsonify({'messaage':'Description is  required'}), 401)

    new_review =Reviews(title,description,business_id)
    REVIEWS.append(new_review)

    return make_response(jsonify({'message':'Review Added Successfully'}),201)



@biz.route('/api/v1/business/<int:business_id>/reviews', methods=['GET'])
def get_all_reviews(business_id):
    business=[business for business in BUSINESS if business.id==business_id]
    if business:
        business = business[0]
    elif business not in BUSINESS:
            return make_response(jsonify({'message':'Reviews not found'}))
    business_id = business.id
    review  = REVIEWS
    found_business=[{review.id:[{'title':review.title,'description':review.description}]for review in REVIEWS}]
    return make_response(jsonify(found_business),200)
    
 