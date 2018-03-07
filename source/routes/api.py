from flask import Flask, jsonify, abort, request
from source.models.business import Business
from source.models.users import User
import uuid
from passlib.hash import sha256_crypt
import datetime

app = Flask(__name__)
"""
Enables use of token
"""
app.config['SECRET_KEY']="b'409ce0cacf23b39b71faccfcb2f9fc3051c587d6155efa77'"


business_instance=Business()
user_instance = User()
# def add_user(username,email,password,public_id):
#     new_user=dict(username=username,email=email,password=password,public_id=public_id)
#     USERS.append(new_user)
    
@app.route('/api/auth/v1/register', methods=['POST'])
def create_user():
    """
    creates a new user in the list of users
    """
    user=request.get_json()
    email = user['email']
    username = user['username']
    password= user['password']

    if not email or not username or not password:
        return jsonify({'message':'Invalid input, please try again!'})

    password=sha256_crypt.encrypt(str(password))
    user_instance.create_user(id, username, email, password)
    return jsonify({'Message':'User successfully registered'}),201

@app.route('/api/v1/login', methods = ['POST'])
def login():
    """
    if request is validated then user is logged in
    """
    user_request=request.get_json()
    username == user_request['username']
    password  == user_request['password']

    #user =[biz for biz in user_instance.users if biz['username'] ==username and biz['passworrd']==password]
    for user in user_instance.users:
        if user['username'] == username and user['password'] == password:
            user_instance.logged_in= True
            print(user_instance.logged_in)
            return jsonify({'message':'logged in successfully'}), 200
    else:
        return jsonify({'message': 'Username / password ivalid, please try again!'})
      
            


@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    user_instance.users
    return jsonify(user_instance.users), 200

@app.route('/api/v1/business', methods=['POST'])
def register_business():
    new_business = request.get_json()
    businessname = new_business['businessname']
    description=new_business['description']
    category =new_business['category']
    location =new_business['location']

    if not businessname or not description or not category or not location:
         return jsonify({'message':'Invalid input, please try again!'})
    for busines in business_instance.business:
        if busines['businessname'] ==businessname:
            return jsonify({'message':'Business already exists'})

    business_instance.create_business(id,businessname,description,location,category)
    return jsonify({'Message':'Business successfully registered'}),201

    


    
