from flask import jsonify, request, Blueprint

from api.base_model import db
from api.business.models import Business, Reviews
from api.helpers.token import token_required
from api.helpers import validate

biz = Blueprint('biz', __name__)


@biz.route('/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    """Registers non existing businesses"""
    dict_data = request.get_json()
    try:
        data = validate.biz_validator(dict_data)
    except AssertionError as error:
        return jsonify({"message": error.args[0]}) , 401

    """checks if business is duplicate """
    duplicate = Business.query.filter_by(
        businessname=data.get('businessname')).first()

    if not duplicate:
        new_business = Business(businessname=data.get('businessname'),
                                description=data.get('description'),
                                category=data.get('category'), location=data.get('location'),
                                owner_id=current_user.id)
        db.session.add(new_business)
        db.session.commit()
        return jsonify({'message': 'Business successfully registered'}), 201
    return jsonify({'message': 'Business already exists'}), 409


@biz.route('/api/v1/businesses', methods=['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    category = request.args.get('category', '', type=str)
    location = request.args.get('location', '', type=str)
    search = request.args.get('q', '', type=str)

    subquery = Business.query
    filter_params = request.args

    for filter in filter_params:
        valid_filters = ("category", "location", "q")
        if filter not in valid_filters:
            continue
        if filter == "category":
            operator = category
        elif filter == "location":
            operator = location
        elif filter == "q":
            filter = "businessname"
            operator = search

        subquery = subquery.filter(getattr(Business, filter).ilike(
            '%' + operator + '%'))
    
    businesses = subquery.paginate(page, limit, False).items
    found_businesses = [business.obj() for business in businesses]
    return jsonify({"results": found_businesses}), 200


@biz.route('/api/v1/businesses/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular business by id"""
    get_business = Business.query.filter_by(id=business_id).first()
    if not get_business:
        return jsonify({'message': 'Business not found'}), 404
    return jsonify(get_business.obj()), 200


@biz.route('/api/v1/businesses/<int:business_id>', methods=['PUT'])
@token_required
def update_by_id(current_user, business_id):
    dict_data = request.get_json()
    try:
        data = validate.update_validator(dict_data)
    except AssertionError as error:
        return jsonify({"message": error.args[0]})

    check_duplication = Business.query.filter_by(businessname=data.get('businessname')).first()
    if check_duplication:
       return jsonify({'message': 'Business already exist'}), 409

    get_business = Business.query.filter_by(id=business_id).first()
   
    if current_user.id != get_business.owner_id:
        return jsonify({'message': 'You can only update your business'}), 404
    if not get_business:
        return jsonify({'message': 'Business does not exist'}), 200

    for key in data.keys():
        value = data[key]
        setattr(get_business, key, value)
    db.session.commit()
    return jsonify({'message': 'Business successfully updated'}), 200



@biz.route('/api/v1/businesses/<int:business_id>', methods=['DELETE'])
@token_required
def delete_business_by_id(current_user, business_id):
    """Endpoint for deleting requested business by id"""
    get_business=Business.query.filter_by(id=business_id).first()
    if get_business:
        if current_user.id == get_business.owner.id:
            db.session.delete(get_business)
            db.session.commit()
            return jsonify({'message': 'Business successfully deleted'}), 202
        return jsonify({'message': 'You can only delete your business'}), 409
    return jsonify({'message': 'Business does not exists'}), 409


@biz.route('/api/v1/businesses/<int:id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, id):
    dict_data=request.get_json()
    get_business=Business.query.filter_by(id=id).first()
    if get_business:

        try:
            data=validate.review_validator(dict_data)
        except AssertionError as error:
            return jsonify({"message": error.args[0]}) , 401

        business_id=get_business.id
        owner_id=current_user.id
        if owner_id == get_business.owner_id:
            return jsonify({'message': 'You cannot review your Business'})

        new_review=Reviews(title=data.get('title'), review=data.get('review'),
                             business_id=get_business.id, owner_id=current_user.id)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review Added Successfully'}), 201
    return jsonify({'message': 'Business not found'}), 201


@biz.route('/api/v1/businesses/<int:id>/reviews', methods=['GET'])
def get_all_reviews(id):
    get_business=Business.query.filter_by(id=id).first()
    if get_business:
        get_review=Reviews.query.filter_by(business_id=id).all()
        if get_review:
            found_review=[]
            for review in get_review:
                obj={
                    'title': review.title,
                    'review': review.review,
                    'reviewer': review.reviewer.username,
                    'created_at': review.date_created,
                    'updated_at': review.date_modified
                }
                found_review.append(obj)
            return jsonify(found_review)
        return jsonify({'message': 'Reviews not found'}), 404
    return jsonify({'message': 'Business not found'}), 200
