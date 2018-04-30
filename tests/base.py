from source.api.api import app, BUSINESS, USERS, REVIEWS
from source.models.business import Business
from source.models.reviews import Reviews
from unittest import TestCase
import json


class BaseTestCase(TestCase):
    """set app config"""
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        self.business = {
            "businessname": "Techbase", "description": "we sell laptops",
            "category": "electronics", "location": "River road"}

        self.person = {
            'username': 'james muriuki',
            'email': 'james20@yahoo.com',
            'password': 'james7738'
                    }

        self.reviews = {
            'title' : 'your app is awesome',
            'description': 'blabla' 
                        }
    
    def register_user(self):
        """Business registration helper"""
        resp = self.app.post('/api/v1/auth/register',
        data = json.dumps(self.person),
        headers = {'content-type': "application/json"})   
        return resp

    def login_user(self):
        """User login helper"""
        resp = self.app.post('/api/v1/auth/login', 
        data=json.dumps(self.person), 
        headers={'content-type': "application/json"})
        return resp

    def business_registration(self):
        """ Business registration helper"""
        resp=self.app.post('/api/v1/business', 
        data=json.dumps(self.business), 
        headers = {'content-type': 'application/json'})
        return resp

    def new_review(self):
        """Review Helper"""
        resp = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(self.reviews), 
        headers={'content-type': 'application/json'})
        return resp     


    def tearDown(self):
        USERS.clear()
        BUSINESS.clear()
        REVIEWS.clear()
        Business.count = 0
        Reviews.count = 0
