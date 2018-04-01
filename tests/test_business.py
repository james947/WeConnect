from source.routes.api import app
from unittest import TestCase
import json


class TestIntegrations(TestCase):
    """set app config"""
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.business = {
            "businessname": "Techbase",
            "description": "we sell laptops",
            "category": "electronics",
            "location": "River road"
            }

        self.business2 = {
            "businessname": "",
            "description": "we sell laptops",
            "category": "electronics",
            "location": "River road"
                }


    def test_business_registration(self):
        """ 
        test business successfully is registered

        """
        response = self.app.post('/api/v1/business', data=json.dumps(self.business), headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Business successfully registered", response_msg["Message"])

    # def test_returns_all_businesses(self):
    #     """ 
    #     test all businesses are returned
    #     """
    #     response = self.app.post('/api/v1/business', data=json.dumps(self.business), headers={'content-type':'application/json'})
    #     self.assertEqual(response.status_code, 201)
    #     response = self.app.get('/api/v1/business')
    #     self.assertIn("Techbase", response.data)
        

    # def test_api_can_get_business_by_id(self):
    #     """
    #     get business by id

    #     """
    #     self.app.post('/api/v1/business', data=self.business)
    #     response = self.app.get('/api/v1/business/0')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content_type, 'application/json')

    # def test_get_by_ivalid_id(self):
    #     """
    #     tests if the id is not valid
    #     """
    #     response = self.app.post('/api/v1/business', data=json.dumps(self.business), headers={'content-type':'application/json'})
    #     self.assertEqual(response.status_code, 201)
    #     response = self.app.get('/api/v1/business/4')
    #     self.assertEqual(response.status_code, 404)
    #     response_msg = json.loads(response.decode.data("UTF-8"))
    #     self.assertIn("Business not found", response_msg["Message"])

    def test_add_empty_business_name(self):
        """
        tests addition of a empty business name
        """
        response = self.app.post('/api/v1/business', data=json.dumps(dict(businessname="",description="yoyo",category="blabla",location="runda")),headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business name required", response_msg['message'])

    def test_add_empty_business_category(self):
        # tests addition of a null category
        response = self.app.post('/api/v1/business', data=json.dumps(dict(businessname="techbase", description="we sell laptops", category="", location="juja")),content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Category is required", response_msg['message'])

    def test_add_empty_business_location(self):
        # tests addition of a null location
        response = self.app.post('/api/v1/business',
                                data=json.dumps(dict(businessname="techbase", description="we sell laptops", category="electronics", location="")),content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Location is required", response_msg['message'])

    def test_add_empty_business_description(self):
        """
        tests addition of a null description
        """
        response = self.app.post('/api/v1/business',data=json.dumps(dict(businessname="techbase", description="", category="electronics", location="juja")),content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Description is  required",response_msg['message'])

    # def test_business_can_be_edited(self):
    #     """
    #     tests if business posted can be edited
    #     """
    #     response = self.app.post('/api/v1/business',
    #                              data=json.dumps(dict(businessname="techbase", description="we sell laptops", category="electronics", location="juja")), content_type="application/json")
    #     response = self.app.put('/api/v1/business/0',
    #                             data=json.dumps(dict(businessname="Ramtoms", description="sell iron boxes", category="electronics", location="juja")),)
    #     self.assertEqual(response.status_code, 200)
    #     results = self.app.get('/api/v1/business/0')
    #     self.assertIn(results.content_type, 'application/json')

    def test_delete(self):
        """test API can delete business"""
        self.app.post('/api/v1/business',data=json.dumps(dict(businessname="techbase", description="we sell laptops", 
                                        category="electronics", location="juja")),content_type="application/json")
        response=self.app.delete('/api/v1/business/0')
        self.assertEqual(response.status_code, 202)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Business successfully deleted", response_msg["message"])


    def teardown(self):
        del self.business
        pass
