from source.api import app
from unittest import TestCase
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.business = {
            "businessname":"Techbase",
            "description":"we sell laptops",
            "category":"electronics",
            "location":"River road"
                        }
    def teardown(self):
        del self.business
        pass



    def test_business_registration(self):
    """test business successfully is registered """
    response=self.app.post('http://127.0.0.1:5000/api/auth/v1/business', data=self.business)
    self.assertEqual(response.status_code,200)
    response_msg = json.loads(response.data.decode("UTF-8"))
    self.assertIn("Business successfully registered", response_msg["Message"]) 

    def test_returns_all_businesses(self):
    """test all businesses are returned"""
    response=self.app.post('http://127.0.0.1:5000/api/auth/v1/business', data=self.business)
    self.assertEqual(response.status_code,201)
    response = self.app.get('http://127.0.0.1:5000/api/auth/v1/business')
    self.assertIn('we sell laptops', str(response.data))

    def test_api_can_get_business_by_id(self):
    response = self.app.post('http://127.0.0.1:5000/api/auth/v1/business')
    self.assertEqual(response.status_code,201)

