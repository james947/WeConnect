from source.api import app
from unittest import TestCase
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def teardown(self):
        pass

    def test_users_in_data(self):
        """returns users in the system"""
        response = self.app.get('http://127.0.0.1:5000/api/v1/users')
        self.assertEqual(response.status_code,200)

    def test_users_registration(self):    
        """tests user registration in the system"""
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register', data=json.dumps(dict(username="test122",password=122)),content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("User successfully registered", response_msg["Message"]) 

    def test_login(self):
        """returns correct login"""
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login',
        data=json.dumps(dict(username="test122",password=122)),content_type="application/json")
        self.assertEqual(response.status_code,201)
        

    def test_return_all_business(self):
        response =self.app.get('http://127.0.0.1:5000/api/v1/business')
        self.assertEqual(response.status_code,200)

    def test_return_one_business(self):
        response =self.app.get('http://127.0.0.1:5000/api/v1/business/1')
        self.assertEqual(response.status_code,200)
    

