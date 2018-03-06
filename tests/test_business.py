from source.routes.api import app
from unittest import TestCase
import json


class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.business = {
            "id": 1,
            "businessname": "Techbase",
            "description": "we sell laptops",
            "category": "electronics",
            "location": "River road"
        }

    def teardown(self):
        del self.business
        pass

    def test_business_registration(self):
        """ 
        test business successfully is registered

        """
        response = self.app.post(
            '/api/auth/v1/business', data=self.business)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business successfully registered",
                      response_msg["Message"])

    def test_returns_all_businesses(self):
        """ 
        test all businesses are returned

        """
        response = self.app.post(
            '/api/auth/v1/business', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/api/auth/v1/business')
        self.assertIn('we sell laptops', str(response.data))

    def test_api_can_get_business_by_id(self):
        """
        get business by id

        """
        response = self.app.post(
            '/api/auth/v1/business', data=self.business)
        self.assertEqual(response.status_code, 201)
        result_in_json = json.loads(
            response.data.decode('utf-8').replace("'", "\""))
        result = self.app.get(
            '/api/auth/v1/business/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('we sell laptops', str(result.data))
        
    def test_get_bad_request(self):
        """
        test if bad request is passed
        """
        response = self.app.get(
            '/api/auth/v1/business/biz')
        self.assertEqual(response.status.code, 400)

    def test_get_by_ivalid_id(self):
        """
        tests if the id is not valid
        """
        response = self.app.post(
            '/api/auth/v1/business', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/api/auth/v1/business/4')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("Business not found", response_msg["Message"])

    def test_add_empty_business_name(self):
        """
        tests addition of a null name
        """
        response = self.app.post('/api/auth/v1/business',
                                data=dict(businessname="", description="we sell laptops", category="electronics", location="juja"))
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business name cannot be empty", response_msg['Message'])

    def test_add_empty_business_category(self):
        # tests addition of a null category
        response = self.app.post('/api/auth/v1/business',
                                data=dict(businessname="techbase", description="we sell laptops", category="", location="juja"))
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Category name cannot be empty", response_msg['Message'])

    def test_add_empty_business_location(self):
        # tests addition of a null location
        response = self.app.post('/api/auth/v1/business',
                                data=dict(businessname="techbase", description="we sell laptops", category="electronics", location=""))
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Location name cannot be empty", response_msg['Message'])

    def test_add_empty_business_description(self):
        """
        tests addition of a null description
        """
        response = self.app.post('/api/auth/v1/business',
                                data=dict(businessname="techbase", description="", category="electronics", location="juja"))
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Description name cannot be empty",
                      response_msg['Message'])

    def test_business_can_be_edited(self):
        """
        tests if business posted can be edited
        """
        response = self.app.post('/api/auth/v1/business',
                                 data=dict(businessname="techbase", description="we sell laptops", category="electronics", location="juja"))
        self.assertEqual(response.status_code, 201)
        response = self.app.put('/api/auth/v1/business/1',
                                data=dict(businessname="Ramtoms", description="sell iron boxes", category="electronics", location="juja"))
        self.assertEqual(response.status_code, 200)
        results = self.app.get('/api/auth/v1/business/1')
        self.assertIn("sell iron boxes", str(results.data))

    def test_delete(self):
        """test API can delete business"""
        response = self.app.post('/api/auth/v1/business',
                                 data=dict(businessname="techbase", description="we sell laptops", category="electronics", location="juja"))
        self.assertEqual(response.status_code, 201)
        response = self.app.delete('http: // 127.0.0.1: 5000/api/auth/v1/business/1')
        response = self.assertEqual(response.status_code, 200)
        # tests to see if business exists
        response = self.app.get('/api/auth/v1/business/1')
        self.assertEqual(response.status_code, 404)


