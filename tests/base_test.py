from unittest import TestCase
import json

from api import create_app, db


class BaseTestCase(TestCase):
    """set app config"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

        self.business = {"businessname": "Techbase","description": "we sell laptops","category": "electronics","location": "River road"}
        self.business2 = {"businessname": "","description": "we sell laptops","category": "electronics","location": "River road"}     
        self.business3 = {"businessname": "Techbase","description": "we sell laptops","category": "","location": "River road"}
        self.business4 = {"businessname": "Techbase","description": "","category": "electronics","location": "River road"}
        self.business5 = {"businessname": "Techbase","description": "we sell laptops","category": "electronics","location": ""}
        
        self.person = {'username': 'james muriuki','email': 'james20@yahoo.com','password': 'james7738'}
        self.person2 = {'username': '','email': 'james20@yahoo.com','password': 'james7738'}
        self.reviews = {'title': 'your app is awesome','review': 'blabla'}


    def register_user(self):
        """Business registration helper"""
        resp = self.client.post('/api/v1/auth/register',
                                data=json.dumps(self.person),
                                headers={'content-type': "application/json"})
        return resp

    def login_user(self):
        """User login helper"""
        resp = self.client.post('/api/v1/auth/login',
                                data=json.dumps(self.person),
                                headers={'content-type': "application/json"})
        return resp

    def get_access_token(self):
        self.register_user()
        data = self.login_user()
        token = json.loads(data.data.decode("UTF-8"))['token']

        return token

    def business_registration(self):
        """ Business registration helper"""

        token = self.get_access_token()
        business = {
            "businessname": "Techbase",
            "description": "we sell laptops",
            "category": "electronics",
            "location": "River road"
            }
        resp = self.client.post(
            '/api/v1/business',
            headers={'x-access-token': token},
            data=json.dumps(business),
            content_type='application/json'
        )
        return resp

    def new_review(self):
        """Review Helper"""
        resp = self.client.post('/api/v1/business/0/review',
                                data=json.dumps(self.reviews),
                                headers={'content-type': 'application/json'})
        return resp

    def get_token(self):
        self.register_user()
        data = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/business',
                                data=json.dumps(self.business),
                                headers={"x-access-token":data})

        return resp


    def business_registration_without_token(self):
        """ Business registration helper"""
        business = {
            "businessname": "Techbase",
            "description": "we sell laptops",
            "category": "electronics",
            "location": "River road"
            }
        resp = self.client.post(
            '/api/v1/business',
            headers={'x-access-token':''},
            data=json.dumps(business),
            content_type='application/json'
        )
        return resp
   
