from base import BaseTestCase
import json

class TestIntegrations(BaseTestCase):
    """tests for business enpoints"""
    def test_business_registration(self):
        """ test business successfully is registered"""
        self.register_user()
        self.login_user()
        resp = self.business_registration()
        response_msg = json.loads(resp.data.decode())
        self.assertIn("Business successfully registered", response_msg["message"])

    def test_returns_all_businesses(self):
        """test all businesses are returned"""
        self.business_registration()
        resp = self.app.get('/api/v1/business/')
        response_data = json.loads(resp.data.decode('utf-8'))
        registered_business = response_data[0]
        self.assertEqual(registered_business['businessname'], 'Techbase')
        

    # def test_api_can_get_business_by_id(self):
    #     """get business by id"""
    #     self.business_registration()
    #     resp = self.app.get('/api/v1/business/0')
    #     registered_business = response_data[0]
    #     self.assertEqual(registered_business['businessname'], 'Techbase')

    def test_get_by_ivalid_id(self):
        """tests if the get business by invalid id"""
        self.business_registration()
        response = self.app.get('/api/v1/business/4')
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business not found", response_msg["message"])

    def test_add_empty_business_name(self):
        """tests addition of a empty business name"""
        response = self.app.post('/api/v1/business', 
        data =json.dumps(dict(businessname="", description="yoyo", category="blabla", location="runda")),
        headers = {'content-type': 'application/json'})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Businessname is required", response_msg['message'])

    def test_add_empty_business_category(self):
        """tests addition of a null category"""
        response = self.app.post('/api/v1/business', 
        data=json.dumps(dict(businessname="techbase", description="we sell laptops", category="", location="juja")),
        content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Category is required", response_msg['message'])

    def test_add_empty_business_location(self):
        # tests addition of a null location
        response = self.app.post('/api/v1/business', 
        data = json.dumps(dict(businessname="techbase", description="we sell laptops", category="electronics", location="")),
         content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Location is required", response_msg['message'])

    def test_add_empty_business_description(self):
        """tests addition of a null description"""
        response = self.app.post('/api/v1/business', 
        data=json.dumps(dict(businessname="techbase", description="", category="electronics", location="juja")),
        content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Description is required",response_msg['message'])

    def test_business_can_be_edited(self):
        """tests if business posted can be edited"""

        self.register_user()
        self.login_user()
        self.business_registration()
        response = self.app.put('/api/v1/business/0',
        data=json.dumps(dict(businessname="Ramtoms", description="sell iron boxes", category="electronics", location="juja")), 
        content_type="application/json")
        results = self.app.get('/api/v1/business/0')
        self.assertIn(results.content_type, 'application/json')

    def test_delete(self):
        """test API can delete business"""
        self.register_user()
        self.login_user()
        resp=self.business_registration()
        print(resp)
        response=self.app.delete('/api/v1/business/0')
        response_msg = json.loads(response.data.decode())
        self.assertIn("Business successfully deleted", response_msg["message"])

