from source.routes.api import app
import unittest 
from source.models.users import User


import json
class TestUsersTestcase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.person={
            'username':'james muriuki',
            'email':'james20@yahoo.com',
            'password':'123456'
                    }



    def test_get_all_users(self):
        """
        returns users in the system

        """
        response = self.app.get('/api/v1/users', data=json.dumps(self.person), headers={'content-type':"application/json"})
        result=json.loads(response.data.decode()) 
        self.assertEqual(response.status_code,200)

    def test_users_registration_empty_username(self):    
        """
        tests user registration in the system

        """
        #implement on this
        response = self.app.post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        if self.person['username'] == "":
            self.assertEqual(response.status_code,401)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertIn("'Username is required'!'",response_msg["message"])

    def test_users_registration_empty_password(self):  
        """tests if registartion password is empty"""
        response = self.app.post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        print(response)
        if self.person['password'] == "": 
            self.assertEqual(response.status_code,401)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertIn('Password is required',response_msg["message"])

    def test_users_registration_empty_email(self):
        """tests if registartion email is empty"""        
        response = self.app.post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        if self.person['email'] == "":
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertEqual(response.status_code,401)
            self.assertIn("Email is required",response_msg["message"])

    def test_users_registration_correct_login(self):
        """tests  correct login registaartion"""
        response = self.app.post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        response_msg=json.loads(response.data.decode())        
        self.assertEqual(response.status_code,201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("User successfully registered", response_msg["Message"])

    def test_users_registration_correct_login(self):
        """tests  correct login registaartion"""
        response = self.app.post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        response_msg=json.loads(response.data.decode())        
        self.assertEqual(response.status_code,201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("User successfully registered", response_msg["Message"])



     
    def test_login(self):
        """
        returns correct login

        """
        response= self.app.post('/api/auth/v1/login', data=json.dumps(self.person), headers={'content-type':"application/json"})
        self.assertEqual(response.status_code,200)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Successful Logged in",response_msg["message"])
        

    def test_login_without_user_email(self):
        """
        tests if API returns an error upon login without username

        """
        response= self.app.post('/api/auth/v1/login',
        data=self.person,content_type="application/json")
        if self.person['email'] =="":
            self.assertEqual(response.status_code,401)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertIn("Email is required",response_msg["message"])
            
        


    def test_login_with_an_empty_password(self):
        """
        test if API returns an error upon login with a null password

        """
        response = self.app.post('/api/auth/v1/login',data=self.person,content_type="application/json")
        if self.person['password'] =="":
            self.assertEqual(response.status_code,401)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertIn("Password is required",response_msg["message"])

    # def test_login_with_a_wrong_password(self):
    #     """
    #     tests API if login Works With A wrong password

    #     """
    #     response = self.app.post('/api/auth/v1/register',
    #     data=json.dumps(dict(email="james@gmail.com",password=122)),content_type="application/json")
    #     response= self.app.post('/api/auth/v1/login',
    #     data=json.dumps(dict(email="james@gmail.com",password=555)),content_type="application/json")
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertEqual(response.status_code,401)
    #     self.assertIn("Password not correct",response_msg["message"])

    def test_login_with_a_wrong_email(self):
        """
        tets if API accepts login with a wrong username

        """
        response= self.app.post('/api/auth/v1/login',
        data=json.dumps(dict(email="james",password=122)),content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Email is invalid', response.data)
        self.assertEqual(response.status_code,401)
        # self.assertIn("Email is invalid",response_msg["message"])


    def teardown(self):
        del self.person


if __name__ == '__main__':
     app.run(debug=True)