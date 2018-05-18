import json
from .base_test import BaseTestCase


class TestUsersTestcase(BaseTestCase):

    def test_users_registration_empty_username(self):
        """tests if  username is empty"""
        response=self.client.post('/api/v1/auth/register', data =json.dumps(self.person2), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertEqual("username is required", response_msg["message"])

    def test_users_registration_empty_password(self):  
        """tests if password is empty"""
        response = self.client.post('/api/v1/auth/register', data =json.dumps(dict(username="james", email="jim@gamil.com", password="")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('password is required',response_msg["message"])

    def test_users_registration_empty_email(self):
        """tests if email is empty"""        
        response = self.client.post('/api/v1/auth/register', data =json.dumps(dict(username="james", email= "", password="12345")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("email is required",response_msg["message"])

    def test_users_registration_duplicate_email(self):
        """tests if email is empty"""        
        reg = self.register_user()
        reg2 = self.register_user()
        response_msg = json.loads(reg2.data.decode("UTF-8"))
        self.assertIn("Email is already registered", response_msg["message"])

    def test_users_registration_invalid_email(self):
        """tests if email is invalid"""        
        response = self.client.post('/api/v1/auth/register', data =json.dumps(dict(username="james", email= "james", password="12345")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Email is invalid",response_msg["message"])

    def test_users_registration_correct_registration(self):
        """tests  correct login registration"""
        response = self.client.post('/api/v1/auth/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))      
        self.assertEqual("User successfully registered", response_msg["Message"])
     
    def test_login(self):
        """returns correct login """
        reg = self.register_user()
        login = self.login_user()
        rsp = json.loads(login.data.decode("UTF-8"))
        self.assertTrue(rsp)

    def test_login_with_a_wrong_email(self):
        """returns correct login """
        reg = self.register_user()
        login = self.client.post('/api/v1/auth/login', data=json.dumps(dict(email="jamesbond@gmail.com", password="james12345")), headers={'content-type':"application/json"})
        response_msg = json.loads(login.data.decode("UTF-8"))
        self.assertEqual("Email not found please try again", response_msg["message"])

    def test_login_with_a_wrong_password(self):
        """tests API if login Works With A wrong password"""
        reg = self.register_user()    
        login= self.client.post('/api/v1/auth/login',data=json.dumps(dict(email="james20@yahoo.com",password="james555")),content_type="application/json")
        response_msg = json.loads(login.data.decode("UTF-8"))
        self.assertEqual("Wrong Password", response_msg["message"])

    def test_validate_login__empty_user_email(self):
        "tests if an empty space is passed"
        self.register_user()
        response=self.client.post('/api/v1/auth/login', 
        data =json.dumps(dict(email="   ", password="james7738")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("email is required", response_msg["message"])


    def test_validate_empty__login_user_password(self):
        "tests if an empty space is passed"
        self.register_user()
        response=self.client.post('/api/v1/auth/login', 
        data =json.dumps(dict(email="james20@yahoo.com", password="    ")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("password is required", response_msg["message"])

    def test_users_login_invalid_email(self):
        """tests if email is invalid"""        
        response = self.client.post('/api/v1/auth/login', data =json.dumps(dict(email= "james", password="12345")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Email is invalid",response_msg["message"])
