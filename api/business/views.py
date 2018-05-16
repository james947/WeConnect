from flask import jsonify, request, Blueprint

from api.baseModel import db
"""import model classes"""
from api.business.models import Business, Reviews
from api.helpers.token import token_required
from api.helpers import validate

biz = Blueprint('biz', __name__)


@biz.route('/api/v1/business', methods=['POST'])
@token_required
def register_business(current_user):
    """Registers non existing businesses"""
    dict_data = request.get_json()

    try:
        data = validate.biz_validator(dict_data)
    except AssertionError as error:
        return jsonify({"message": error.args[0]})

    """checks if business is duplicate """
    duplicate = Business.query.filter_by(
        businessname=data.get('businessname')).first()

    if not duplicate:
        new_business = Business(businessname=data.get('businessname'),
                                description=data.get('description'),
                                category=data.get('category'), location=data.get('location'), owner_id=current_user.id)
        db.session.add(new_business)
        db.session.commit()
        return jsonify({'message': 'Business successfully registered'}), 201
    return jsonify({'message': 'Business already exists'}), 409


@biz.route('/api/v1/business', methods=['GET'])
def get_all_businesses():
    """Returns the requested business all the registered businesses"""
    businesses = Business.query.all()
    if not businesses:
        return jsonify({'message': 'No business found'}), 401
    found_business = []
    for business in businesses:
        obj = {
            'id': business.id,
            'businessname': business.businessname,
            'description': business.description,
            'category': business.category,
            'owner': business.owner.username,
            'created_at': business.date_created,
            'updated_at': business.date_modified
        }
        found_business.append(obj)
    return jsonify(found_business), 200


@biz.route('/api/v1/business/<int:business_id>', methods=['GET'])
def get_by_id(business_id):
    """Gets a particular business by id"""
    get_business = Business.query.filter_by(id=business_id).first()
    if not get_business:
        return jsonify({'message': 'Business not found'}), 404
    found_business = []
    obj = {
        'id': get_business.id,
        'businessname': get_business.businessname,
        'description': get_business.description,
        'category': get_business.category,
        'location': get_business.location,
        'owner': get_business.owner.username,
        'created_at': get_business.date_created,
        'updated_at': get_business.date_modified
    }
    found_business.append(obj)
    return jsonify(found_business), 200


@biz.route('/api/v1/business/<int:business_id>', methods=['PUT'])
@token_required
def update_by_id(current_user, business_id):
    """"updates business by id"""
    get_business = Business.query.filter_by(id=business_id).first()
    if get_business:
        if current_user.id == get_business.owner_id:
            duplicate = Business.query.filter_by(
                businessname=get_business.businessname).first()
            if duplicate:
                get_business.businessname = request.json['businessname']
                get_business.description = request.json['description']
                get_business.category = request.json['category']
                get_business.location = request.json['location']
                db.session.add(get_business)
                db.session.commit()
                return jsonify({'message': 'Business successfully updated'}), 200
            return jsonify({'message': 'Business already exists'}), 409
        return jsonify({'message': 'You can only Update your business'}), 409
    return jsonify({'message': 'Business does not exists'}), 404


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
            return jsonify({'message': 'Business successfully deleted'}), 202
        return jsonify({'message': 'You can only delete your business'}), 409
    return jsonify({'message': 'Business does not exists'}), 409


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
            return jsonify({'message': 'Title is required'}), 401
        elif review == "":
            return jsonify({'messaage': 'Description is  required'}), 401

        new_review = Reviews(title=title, review=review,
                             business_id=get_business.id, owner_id=current_user.id)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review Added Successfully'}), 201
    return jsonify({'message': 'Business not found'}), 201


@biz.route('/api/v1/business/<int:id>/reviews', methods=['GET'])
def get_all_reviews(id):
    get_business = Business.query.filter_by(id=id).first()
    if get_business:
        get_review = Reviews.query.filter_by(business_id=id)
        if get_review:
            found_review = []
            for review in get_review:
                obj = {
                    'title': review.title,
                    'review': review.review,
                    'reviewer': review.reviewer.username,
                    'created_at': review.date_created,
                    'updated_at': review.date_modified
                }

                found_review.append(obj)
                return jsonify(found_review)
        return jsonify({'message': 'Reviews not found'})
    return jsonify({'message': 'Business not found'}), 200
