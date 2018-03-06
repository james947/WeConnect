from source.routes.api import app
from unittest import TestCase
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.reviews = {
            'title':"App on point",
            'descritpion':'Your app is awesome',
        }
    
    def teardown(self):
        del self.reviews

    def test_add_new_review(self):
        """
        Api creates a new review

        """
        response=self.app.post('/api/auth/v1/business/1/reviews', data=self.reviews)
        self.assertEqual(response.status_code,201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("review added", response_msg["Message"]) 

    def test_add_null_review_title(self):
        """"
        tests APi result if preview title is null
        """
        response = self.app.post('/api/auth/v1/business/1/reviews',data=dict(title="",descritpion="Your app is great"))
        self.assertEqual(response.status_code,403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Title is required", response_msg["Message"]) 

    def test_add_null_review_description(self):
        """"
        tests APi result if preview title is null
        """
        response = self.app.post('/api/auth/v1/business/1/reviews',data=dict(title="",descritpion="Your app is great"))
        self.assertEqual(response.status_code,404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Title is required", response_msg["Message"]) 


    def test_get_review(self):
        """
        Test if APi gets review

        """
        response=self.app.post('/api/auth/v1/business/1/reviews', data=self.reviews)
        self.assertEqual(response.status_code,201) 
        response=self.app.get('/api/auth/v1/business/1/reviews/1')
        response = self.assertEqual(response.status_code,200)

    def test_get_invalid_review(self):
        """
        Tests Api when request is invalid
        """
        response=self.app.post('/api/auth/v1/business/1/reviews', data=self.reviews)
        self.assertEqual(response.status_code,201)
        response=self.app.get('/api/auth/v1/business/1/reviews/5')
        response = self.assertEqual(response.status_code,400)

    def test_update_review(self):
        """
        tests if APi updates review
        """
        response=self.app.post('/api/auth/v1/business/1/reviews', data=dict(title="your app",descritpion="it is awesome"))
        self.assertEqual(response.status_code,201)
        response=self.app.put('/api/auth/v1/business/1/reviews/1', data=dict(title="your app",descritpion="Has bugs"))
        self.assertEqual(response.status_code,200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("review updated", response_msg["Message"]) 
    
    def test_delete_review(self):
        """
        Tests Api deletes review
        """
        response=self.app.post('/api/auth/v1/business/1/reviews', data=dict(title="your app",descritpion="it is awesome"))
        self.assertEqual(response.status_code,201)
        response=self.app.delete('/api/auth/v1/business/1/reviews/1')
        self.assertEqual(response.status_code,200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("review deleted", response_msg["Message"])
        
