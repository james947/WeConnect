from source.api import app
from unittest import TestCase
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.person={
            'username':'james muriuki',
            'email':'james20@yahoo.com',
            'password':'123456'
                    }

    def teardown(self):
        del self.person
        pass

    def test_users_in_data(self):
        """returns users in the system"""
        response = self.app.get('http://127.0.0.1:5000/api/v1/users')
        self.assertEqual(response.status_code,200)

    def test_users_registration(self):    
        """tests user registration in the system"""
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=self.person,content_type="application/json")
        self.assertEqual(response.status_code,201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("User successfully registered", response_msg["Message"]) 
    
    def test_if_null_registration_username(self):
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=dict(name="",email="james20@yahoo.com",password=123456),content_type="application/json")
        self.assertEqual(response.status_code,400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Username cannot be null",response_msg["Message"])
        
    def test_if_null_registration_password(self):
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=dict(name="james",email="james20@yahoo.com",password=""),content_type="application/json")
        self.assertEqual(response.status_code,400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Password cannot be null",response_msg["Message"])  

    def test_login(self):
        """returns correct login"""
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login',
        data=json.dumps(dict(username="test122",password=122)),content_type="application/json")
        self.assertEqual(response.status_code,200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Successful Logged in",response_msg["Message"])
        
    def test_login_without_user_name(self):
        """tets if API returns an error upon login without username"""
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=dict(username="test122",password=122),content_type="application/json")
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login',
        data=dict(username="",password=122),content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response.status_code,400)
        self.assertIn("Username cannot be null",response_msg["Message"])

    def test_login_with_an_empty_password(self):
        """test if API returns an error upon login with a null password"""
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=dict(username="test122",password=122),content_type="application/json")
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login',
        data=dict(username="test122",password=""),content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response.status_code,400)
        self.assertIn("Password cannot be null",response_msg["Message"])

    def test_login_with_a_wrong_password(self):
        """tests API if login Works With A wrong password"""
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=dict(username="test122",password=122),content_type="application/json")
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login',
        data=dict(username="test122",password=555),content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response.status_code,400)
        self.assertIn("Password not correct",response_msg["Message"])

    def test_login_with_a_wrong_username(self):
        """tets if API accepts login with a wrong username"""
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/register',
        data=dict(username="test122",password=122),content_type="application/json")
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login',
        data=dict(username="james",password=555),content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response.status_code,400)
        self.assertIn("Password not correct",response_msg["Message"])


