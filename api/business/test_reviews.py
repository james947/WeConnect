import json
import unittest
from source.routes.api import create_app, db
from source.routes.auth import views


class TestUsersTestcase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.reviews = {'title': 'App on point','review':  'Your app is awesome'}
        self.person = {'username':'james', 'email':'jima@gmail.com', 'password':'12345'}
        self.business = {'businessname':'techbase', 'description':'sell cars', 'category':'cars', 'location':'mombasa road'}

    def test_add_new_review(self):
        """
        Api creates a new review
        """
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode())
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business), content_type="application/json", headers={"x-access-token":token})
        resp=self.client().post('/api/v1/business/1/review', data=json.dumps(self.reviews), content_type="application/json" ,headers={"x-access-token":token})
        response_msg = json.loads(resp.data.decode())
        self.assertIn("Review Added Successfully", response_msg["message"]) 

    def test_add_null_review_title(self):
        """testsif review title is empty"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode())
        token = data['token']
        resp = self.client().post('/api/v1/business', data=json.dumps(self.business), content_type="application/json", headers={"x-access-token":token})
        response = self.client().post('/api/v1/business/1/review', data=json.dumps(dict(title="", review="Your app is great")), content_type="application/json", headers={"x-access-token":token})
        response_msg = json.loads(response.data.decode())
        self.assertIn("Title is required", response_msg["message"]) 

#     def test_add_null_review_description(self):
#         """"
#         tests APi result if preview title is null
#         """
#         response = self.app.post('/api/auth/v1/business/1/reviews',data=dict(title="",descritpion="Your app is great"))
#         self.assertEqual(response.status_code,401)
#         response_msg = json.loads(response.data.decode())
#         self.assertIn("Title is required", response_msg["Message"]) 


#     def test_get_review(self):
#         """
#         Test if APi gets review
#         """
#         response=self.app.post('/api/auth/v1/business/1/reviews', data=self.reviews)
#         self.assertEqual(response.status_code,201) 
#         response=self.app.get('/api/auth/v1/business/1/reviews/1')
#         response = self.assertEqual(response.status_code,200)

#     def test_get_invalid_review(self):
#         """
#         Tests Api when request is invalid
#         """
#         response=self.app.post('/api/auth/v1/business/1/reviews', data=self.reviews)
#         self.assertEqual(response.status_code,201)
#         response=self.app.get('/api/auth/v1/business/1/reviews/5')
#         response = self.assertEqual(response.status_code,400)

#     def test_update_review(self):
#         """
#         tests if APi updates review
#         """
#         response=self.app.post('/api/auth/v1/business/1/reviews', data=dict(title="your app",descritpion="it is awesome"))
#         self.assertEqual(response.status_code,201)
#         response=self.app.put('/api/auth/v1/business/1/reviews/1', data=dict(title="your app",descritpion="Has bugs"))
#         self.assertEqual(response.status_code,200)
#         response_msg = json.loads(response.data.decode())
#         self.assertIn("review updated", response_msg["Message"]) 
    
#     def test_delete_review(self):
#         """
#         Tests Api deletes review
#         """
#         response=self.app.post('/api/auth/v1/business/1/reviews', data=dict(title="your app",descritpion="it is awesome"))
#         self.assertEqual(response.status_code,201)
#         response=self.app.delete('/api/auth/v1/business/1/reviews/1')
#         self.assertEqual(response.status_code,200)
#         response_msg = json.loads(response.data.decode())
#         self.assertIn("review deleted", response_msg["Message"])
        


    
#     def test_users_registration_empty_username(self):    
#         """
#         tests user registration in the system
#         """
#         #implement on this
#         response = self.app.post('/api/auth/v1/register', data=json.dumps(self.reviews), headers={'content-type':"application/json"})
#         if self.reviews['username'] == "":
#             self.assertEqual(response.status_code,401)
#             response_msg = json.loads(response.data.decode())
#             self.assertIn("'Username is required'!'",response_msg["message"])

#     def teardown(self):
#         del self.reviews


