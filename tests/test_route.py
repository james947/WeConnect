from source.routes.api import app
import unittest 
from source.models.users import User
import json
class TestUsersTestcase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.person={
            'username':'james muriuki',
            'email':'james20@yahoo.com',
            'password':'123456'
                    }

    def test_users_registration_empty_username(self):
        response=self.app.post('/api/auth/v1/register',data =json.dumps(dict(username="", email="jim@gamil.com", password="12345")), headers={'content-type':"application/json"})
        self.assertEqual(response.status_code,401)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username is required",response_msg["message"])

    def test_users_registration_empty_password(self):  
        """tests if registartion password is empty"""
        response = self.app.post('/api/auth/v1/register', data =json.dumps(dict(username="james", email="jim@gamil.com", password="")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Password is required',response_msg["message"])

    def test_users_registration_empty_email(self):
        """tests if registartion email is empty"""        
        response = self.app.post('/api/auth/v1/register', data =json.dumps(dict(username="james", email="", password="12345")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response.status_code,401)
        self.assertIn("Email is required",response_msg["message"])

    def test_users_registration_correct_registration(self):
        """tests  correct login registration"""
        response = self.app.post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        self.assertEqual(response.status_code,201)      
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("User successfully registered", response_msg["Message"])
     
    def test_login(self):
        """returns correct login """
        register = self.app.post('/api/auth/v1/register', data=json.dumps(dict(username="james",email="james@gmail.com",password="12345")), headers={'content-type':"application/json"})
        login= self.app.post('/api/v1/login', data=json.dumps(dict(email="james@gmail.com",password="12345")), headers={'content-type':"application/json"})
        self.assertEqual(login.status_code,200)
        response_msg = json.loads(login.data.decode("UTF-8"))
        self.assertIn("logged in successfully",response_msg["message"])


    # def test_login_with_a_wrong_password(self):
    #     """
    #     tests API if login Works With A wrong password

    #     """
    #     register = self.app.post('/api/auth/v1/register', data=json.dumps(dict(username="james",email="james@gmail.com",password="12345")), headers={'content-type':"application/json"})     
    #     login= self.app.post('/api/v1/login',data=json.dumps(dict(email="james@gmail.com",password="555")),content_type="application/json")
    #     self.assertEqual(login.status_code,401)
    #     response_msg = json.loads(login.data.decode("UTF-8"))
    #     self.assertIn("Password not correct",response_msg["message"])

    # def test_login_with_a_wrong_email(self):
    #     """tests if API accepts login with a wrong email"""
    #     login= self.app.post('/api/v1/login',
    #     data=json.dumps(dict(email="james",password="122")),content_type="application/json")
    #     self.assertEqual(login.status_code,401)
    #     response_msg = json.loads(login.data.decode("UTF-8"))
    #     self.assertIn("Email is invalid", response_msg["message"])


    def teardown(self):
        del self.person


