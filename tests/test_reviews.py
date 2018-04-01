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

    # def test_add_null_review_title(self):
    #     """"
    #     tests APi result if preview title is null
    #     """
    #     response = self.app.post('/api/v1/business/1/review',data=json.dumps(dict(title="",description="Your app is great")),content_type="application/json")
    #     self.assertEqual(response.status_code,401)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("Title is required", response_msg["Message"]) 

    # def test_add_null_review_description(self):
    #     """"
    #     tests APi result if preview title is null
    #     """
    #     response = self.app.post('/api/v1/business/1/reviews',data=json.dumps(dict(title="app",descritpion="")), content_type="application/json")
    #     self.assertEqual(response.status_code,401)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("Description is  required", response_msg["Message"]) 


    def test_get_review(self):
        """
        Test if APi gets review

        """
        response=self.app.post('/api/v1/business/1/review', data=json.dumps(dict(title="app", description="yoyo")), content_type="application/json")
        self.assertEqual(response.status_code,201) 
        response=self.app.get('/api/v1/business/1/reviews/1')
        response_msg= json.loads(response.data.decode("UTF-8"))
        self.assertIn("Your app is awesome", response_msg.data)

#     def test_get_invalid_review(self):
#         """
#         Tests Api when request is invalid
#         """
#         response=self.app.post('/api/auth/v1/business/1/reviews', data=self.reviews)
#         self.assertEqual(response.status_code,201)
#         response=self.app.get('/api/auth/v1/business/1/reviews/5')
#         response = self.assertEqual(response.status_code,400)


    

    