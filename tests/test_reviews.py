from source.routes.api import app
from unittest import TestCase
import json

from base import BaseTestCase
import json



class TestIntegrations(BaseTestCase):

    def test_add_new_review(self):
        """Api creates a new review"""
        self.login_user()
        self.register_user()
        self.business_registration()
        response = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(dict(title="app", description="yoyo")), 
        content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Review Added Successfully", response_msg["message"]) 

    # def test_add_empty_review_title(self):
    #     """"tests_ if review_title is empty"""
    #     self.login_user()
    #     self.register_user()
    #     self.business_registration()
    #     response = self.app.post('/api/v1/business/0/review', 
    #     data=json.dumps(dict(title="", description="Your app is great")), 
    #     content_type="application/json")
    #     self.assertEqual(response.status_code, 401)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("Title is required", response_msg["Message"]) 


    def test_add_empty_review_description(self):
        """"tests if review_description is empty"""
        self.login_user()
        self.register_user()
        self.business_registration()
        response = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(dict(title="app",description="")), 
        content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Description is required", response_msg["message"]) 

    def test_get_review(self):
        """Test if APi gets review."""
        self.business_registration()
        self.login_user()
        self.register_user()
        resp = self.new_review()
        response_msg = json.loads(resp.data.decode())
        self.assertIn("Review Added Successfully", response_msg["message"]) 
        # self.assertEqual("Your app is awesome", response[0]['0']['description'])



    

    