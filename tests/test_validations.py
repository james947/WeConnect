from .base_test import BaseTestCase

import json


class TestUsersTestcase(BaseTestCase):
    """tests for authentication"""
    "testing user data"
    def test_validate_register_user_name(self):
        "tests if the username is valid"
        response=self.client.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="111", email="jim@gmail.com", password="james7738")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username should contain atleast (a-z), (0-4), (-), (_), characters(4)", response_msg["message"])

    def test_validate_register_user_password(self):
        "tests if the password is valid"
        response=self.client.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="james7738", email="jim@gamil.com", password="12345")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("password should contain atleast (a-z), (0-4), (-), characters(8)", response_msg["message"])

    "testing  register key validations"
    def test_validate_key_username(self):
        "tests if key username is empty"
        response=self.client.post('/api/v1/auth/register', 
        data =json.dumps(dict(email="jim@gamil.com", password="12345")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("username is missing", response_msg["message"])
    
    def test_validate_key_email(self):
        "tests if key email is empty"
        response=self.client.post('/api/v1/auth/register', 
        data =json.dumps(dict(username = "james7738", password="12345")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("email is missing", response_msg["message"])

    def test_validate_key_password(self):
        "tests if key password is empty"
        response = self.client.post('/api/v1/auth/register', 
        data = json.dumps(dict(email="jim@gamil.com", username = "james7738")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("password is missing", response_msg["message"])

    "testing  login key validations"
    def test_validate_login_key_password(self):
        "tests if login password_key is empty"
        response=self.client.post('/api/v1/auth/login', 
        data =json.dumps(dict(email="jim@gamil.com")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("password is missing", response_msg["message"])

    def test_validate_login_key_email(self):
        "tests if login_email key is empty"
        response=self.client.post('/api/v1/auth/login', 
        data =json.dumps(dict(password="james7738")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("email is missing", response_msg["message"])

    def test_validate_register_user_password(self):
        "tests if the password is valid"
        response=self.client.post('/api/v1/auth/login', 
        data =json.dumps(dict(username="james7738", email="jim@gamil.com", password="12345")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("password should contain atleast (a-z), (0-4), (-), characters(8)", response_msg["message"])


