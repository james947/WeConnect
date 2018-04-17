from source.routes.api import app, BUSINESS, USERS, REVIEWS
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
            'password': '123456'
                    }
    
    def register_user(self):
        """tests  correct login registration"""
        resp = self.app.post('/api/auth/v1/register', 
        data = json.dumps(self.person), 
        headers = {'content-type': "application/json"})   
        return resp

    def login_user(self):
        """returns correct login """
        resp = self.app.post('/api/v1/login', 
        data = json.dumps(self.person), 
        headers = {'content-type': "application/json"})
        return resp

    def business_registration(self):
        """ test business successfully is registered"""
        resp = self.app.post('/api/v1/business', 
        data = json.dumps(self.business), 
        headers = {'content-type':'application/json'})
        return resp

    def tearDown(self):
        USERS.clear()
        BUSINESS.clear()
        REVIEWS.clear()
