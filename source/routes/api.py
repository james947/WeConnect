from flask import Flask, jsonify, abort, request, make_response,json, session, Blueprint
from functools import wraps
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from source.routes.auth.views import token_required

biz = Blueprint('biz', __name__)
from flask_api import FlaskAPI
#from flask_sqlalchemy import SQLAlchemy
from source.models.models import db

"""import model classes"""
from source.models.models import Users, Business, Reviews


# local import
from instance.config import app_config


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



@biz.route('/api/v1/business', methods=['POST'])
@token_required
def register_business(current_user):
    """Registers non existing businesses"""
    new_business = request.get_json()
    businessname = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']
    
    if businessname == "":
        return make_response(jsonify({'message':'Businessname required'}), 401)
    elif description == "":
        return make_response(jsonify({'message':'Description is  required'}), 401)
    elif category == "":
        return make_response(jsonify({'message':'Category name required'}), 401)
    elif location == "":
        return make_response(jsonify ({'message':'Location name required'}), 401)
    """checks if business is duplicate """
    duplicate = Business.query.filter_by(businessname=businessname).first()

    if  not duplicate:
        new_business=Business(businessname=businessname,description=description,
                              category=category,location=location,owner_id=current_user.id)
        db.session.add(new_business)
        db.session.commit()
        return jsonify({'message':'Business successfully registered'}),201
    return make_response(jsonify({'message':'Business already exists'}),409)
 
   

@biz.route('/api/v1/business', methods= ['GET'])
@token_required
def get_all_businesses(current_user):
    """Returns the requested business all the registered businesses"""
    businesses = Business.query.all()
    if not businesses:
        return jsonify({'message':'No business found'}), 401
    found_business = []
    for business in businesses:
        obj = {
                'id':business.id,
                'businessname':business.businessname,
                'description' :business.description,
                'category': business.category,
                'owner':business.owner.username,
                'created_at': business.date_created,
                'updated_at': business.date_modified
            }
        found_business.append(obj)
    return make_response(jsonify(found_business),200)                


@biz.route('/api/v1/business/<int:business_id>', methods=['GET'])
@token_required
def get_by_id(current_user, business_id):
    """Gets a particular business by id"""
    get_business = Business.query.filter_by(id=business_id).first()
    if not get_business:
        return  make_response(jsonify({'message':'Business not found'}),404)
    found_business = []
    obj = {
        'id':get_business.id,
        'businessname':get_business.businessname,
        'description':get_business.description,
        'category':get_business.category,
        'location':get_business.location,
        'owner':get_business.owner.username,
        'created_at': get_business.date_created,
        'updated_at': get_business.date_modified
         }
    found_business.append(obj)
    return make_response(jsonify(found_business),200)

@biz.route('/api/v1/business/<int:business_id>', methods=['PUT'])
@token_required
def update_by_id(current_user, business_id):
    """"updates business by id"""
    #get business by id then update from the json post request
    get_business = Business.query.filter_by(id=business_id).first()
    if get_business:
        if current_user.id == get_business.owner_id:
            duplicate = Business.query.filter_by(businessname=get_business.businessname).first()
            if duplicate:
                get_business.businessname = request.json['businessname']
                get_business.description = request.json['description']
                get_business.category = request.json['category']
                get_business.location = request.json['location']
                db.session.add(get_business)
                db.session.commit()
                return make_response(jsonify({'message':'Business successfully updated'}), 200)
            return make_response(jsonify({'message':'Business already exists'}), 409)
        return make_response(jsonify({'message':'You can only Update your business'}), 409)
    return make_response(jsonify({'message':'Business does not exists'}), 404)

@biz.route('/api/v1/business/<int:business_id>', methods=['DELETE'])
@token_required
def delete_business_by_id(current_user, business_id):
    """Endpoint for deleting requested business by id"""
    get_business = Business.query.filter_by(id=business_id).first()
    # if current_user.id != get_business.owner_id
        
    if get_business:
        if current_user.id == get_business.owner.id:
            db.session.delete(get_business)
            db.session.commit()
            return jsonify({'message':'Business successfully deleted'}),202
        return make_response(jsonify({'message':'You can only delete your business'}),409)
    return make_response(jsonify({'message':'Business does not exists'}),409)

@biz.route('/api/v1/business/<int:id>/review', methods=['POST'])
@token_required
def add_review(current_user, id):
    new_review = request.get_json()
    get_business = Business.query.filter_by(id=id).first()
    if get_business:

        title = new_review['title']
        review = new_review['review']
        business_id = get_business.id
        owner_id = current_user.id 

        if title == "":
            return make_response(jsonify({'message':'Title is required'}), 401)
        elif review == "":
            return make_response(jsonify({'messaage':'Description is  required'}), 401)

        new_review =Reviews(title=title, review = review, business_id = get_business.id, owner_id = current_user.id)
        db.session.add(new_review)
        db.session.commit()
        return make_response(jsonify({'message':'Review Added Successfully'}),201)
    return make_response(jsonify({'message':'Business not found'}),201)


@biz.route('/api/v1/business/<int:id>/reviews', methods=['GET'])
@token_required
def get_all_reviews(current_user, id):
    get_business = Business.query.filter_by(id=id).first()
    if get_business:
        get_review = Reviews.query.all()
        if get_review:
            found_review = []
            for review in get_review:
                obj = {
                        'title':review.title,
                        'review':review.review,
                        'reviewer':review.reviewer.username,
                        'created_at': review.date_created,
                        'updated_at': review.date_modified
                      }

                found_review.append(obj)
                return make_response(jsonify(found_review))
        return make_response(jsonify({'message':'Reviews not found'}))
    return make_response(jsonify({'message':'Business not found'}),200)
