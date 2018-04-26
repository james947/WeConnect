from base import BaseTestCase
import json


class TestUsersTestcase(BaseTestCase):
    """tests for authentication"""
    def test_validate_register_user_name(self):
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="111", email="jim@gmail.com", password="james7738")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("Username should contain atleast (a-z), (0-4), (-), (_), characters(4)", response_msg["message"])

    def test_validate_register_user_password(self):
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="james7738", email="jim@gamil.com", password="12345")), 
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("password should contain atleast (a-z), (0-4), (-), characters(8)", response_msg["message"])

    def test_validate_key_username(self):
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(email="jim@gamil.com", password="12345")), 
        content_type="application/json")
        print('bxklnkc', response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username is missing", response_msg["message"])
    
    def test_validate_key_email(self):
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username = "james7738", password="12345")), 
        content_type="application/json")
        print('bxklnkc', response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Email is missing", response_msg["message"])

    def test_validate_key_password(self):
        response=self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(email="jim@gamil.com", username = "james7738")), 
        content_type="application/json")
        print('bxklnkc', response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Password is missing", response_msg["message"])

    def test_validate_login_key_password(self):
        response=self.app.post('/api/v1/auth/login', 
        data =json.dumps(dict(email="jim@gamil.com")), 
        content_type="application/json")
        print('bxklnkc', response)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Password is missing", response_msg["message"])

    def test_validate_login_key_email(self):
        response=self.app.post('/api/v1/auth/login', 
        data =json.dumps(dict(password="james7738")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Email is missing", response_msg["message"])

