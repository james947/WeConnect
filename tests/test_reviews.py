from source.routes.api import app
from unittest import TestCase
import json
from passlib.hash import sha256_crypt

class TestIntegrations(TestCase):
    """app test config"""
    def setUp(self):
        self.app = app.test_client()
        self.reviews = {
            'title': "App on point",
            'description':  "Your app is awesome",
        }
    
    def teardown(self):
        del self.reviews

    def test_add_new_review(self):
        """
        Api creates a new review

        """
        response=self.app.post('/api/v1/business/1/review', data=json.dumps(dict(title="app", description="yoyo")), content_type="application/json")
        self.assertEqual(response.status_code,201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Review Added Successfully", response_msg["message"]) 

    def test_add_empty_review_title(self):
        """"tests_ if review_title is empty"""
        response = self.app.post('/api/v1/business/1/review',data=json.dumps(dict(title="", description="Your app is great")),content_type="application/json")
        self.assertEqual(response.status_code,401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Title is required", response_msg["Message"]) 

    def test_add_empty_review_description(self):
        """"tests if review_description is empty"""
        
        response = self.app.post('/api/v1/business/1/review',data=json.dumps(dict(title="app",description="")), content_type="application/json")
        self.assertEqual(response.status_code,401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Description is  required", response_msg["message"]) 


    # def test_get_review(self):
    #     """
    #     Test if APi gets review

    #     """
    #     response=self.app.post('/api/v1/business/1/review', data=json.dumps(dict(title="app", description="yoyo")), content_type="application/json")
    #     self.assertEqual(response.status_code,201) 
    #     response=self.app.get('/api/v1/business/1/reviews/0')
    #     response_msg= json.loads(response.data.decode())
    #     self.assertIn("Your app is awesome", str(response_msg.data))


    

    