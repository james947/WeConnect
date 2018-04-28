from base import BaseTestCase

import json


class TestUsersTestcase(BaseTestCase):
    """tests for authentication"""
    "testing user data"
    def test_validate_register_user_name(self):
        "tests if the username is valid"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="111", email="jim@gmail.com", password="james7738")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username should contain atleast (a-z), (0-4), (-), (_), characters(4)", response_msg["message"])

    def test_validate_register_user_password(self):
        "tests if the password is valid"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="james7738", email="jim@gamil.com", password="12345")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("password should contain atleast (a-z), (0-4), (-), characters(8)", response_msg["message"])

    "testing key validations"
    def test_validate_key_username(self):
        "tests if key username is empty"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(email="jim@gamil.com", password="12345")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username is missing", response_msg["message"])
    
    def test_validate_key_email(self):
        "tests if key email is empty"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username = "james7738", password="12345")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Email is missing", response_msg["message"])

    def test_validate_key_password(self):
        "tests if key password is empty"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(email="jim@gamil.com", username = "james7738")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Password is missing", response_msg["message"])

    def test_validate_login_key_password(self):
        "tests if login password_key is empty"
        response=self.app.post('/api/v1/auth/login', 
        data =json.dumps(dict(email="jim@gamil.com")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Password is missing", response_msg["message"])

    def test_validate_login_key_email(self):
        "tests if login_email key is empty"
        response=self.app.post('/api/v1/auth/login', 
        data =json.dumps(dict(password="james7738")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Email is missing", response_msg["message"])

    "testing empty spaces"
    def test_validate_register_empty__user_email(self):
        "tests if an empty space is passed"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="james254", email="  ", password="james7738")), 
        headers={'content-type':"application/json"})
        print(response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Email is required", response_msg["message"])

    def test_validate_register__empty_user_password(self):
        "tests if an empty space is passed"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="james254", email="james@gmail.com", password="    ")), 
        headers={'content-type':"application/json"})
        print(response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Password is required", response_msg["message"])


    def test_validate_register__empty_user_username(self):
        "tests if an empty space is passed"
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="        ", email="james@gmail.com", password="james7738")), 
        headers={'content-type':"application/json"})
        print(response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username is required", response_msg["message"])


    def test_validate_login__empty_user_username(self):
        "tests if an empty space is passed"
        self.register_user()
        response=self.app.post('/api/v1/auth/login', 
        data =json.dumps(dict(username="        ", email="james20@yahoo.com", password="james7738")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username is required", response_msg["message"])


    def test_validate_empty__login_user_password(self):
        "tests if an empty space is passed"
        self.register_user()
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="james254", email="james20@yahoo.com", password="    ")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("Password is required", response_msg["message"])
