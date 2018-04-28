from base import BaseTestCase

import json


class TestIntegrations(BaseTestCase):
    """tests for business enpoints"""
    def test_business_registration(self):
        """ test business successfully is registered"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register = self.app.post('/api/v1/business', data=json.dumps(dict(businessname="techbase", description="yoyo", category="blabla", location="runda")),  content_type="application/json", headers={"Authorization":"Bearer {}".format(token)})
        response_msg = json.loads(register.data.decode())
        self.assertIn("Business successfully registered", response_msg["message"])

    def test_returns_all_businesses(self):
        """test all businesses are returned"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register =self.app.post('/api/v1/business', 
        data=json.dumps(dict(businessname="Techbase", description="yoyo", 
        category="blabla", location="runda")),  content_type="application/json", 
        headers={"Authorization":"Bearer {}".format(token)})
        resp = self.app.get('/api/v1/business/')
        response_data = json.loads(resp.data.decode('utf-8'))
        registered_business = response_data[0]
        self.assertEqual(registered_business['businessname'], 'Techbase')
        

    def test_api_can_get_business_by_id(self):
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register =self.app.post('/api/v1/business', 
        data=json.dumps(dict(businessname="Techbase", description="yoyo", 
        category="blabla", location="runda")),  content_type="application/json", 
        headers={"Authorization":"Bearer {}".format(token)})
        get = self.app.get('/api/v1/business/0')
        response_data = json.loads(get.data.decode('utf-8'))
        self.assertIn('Techbase', response_data['businessname'])

    def test_get_by_ivalid_id(self):
        """tests if the get business by invalid id"""
        self.business_registration()
        response = self.app.get('/api/v1/business/4')
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business not found", response_msg["message"])

    def test_add_empty_business_name(self):
        """tests addition of a empty business name"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/business', 
        data =json.dumps(dict(businessname="", description="yoyo", category="blabla", location="runda")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Businessname is required", response_msg['message'])

    def test_add_empty_business_category(self):
        """tests addition of a null category"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/business', 
        data =json.dumps(dict(businessname="Techbase", description="yoyo", category="", location="runda")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Category is required", response_msg['message'])

    def test_add_empty_business_location(self):
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/business', 
        data =json.dumps(dict(businessname="Techbase", description="yoyo", category="laptops", location="")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Location is required", response_msg['message'])

    def test_add_empty_business_description(self):
        """tests addition of a null description"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/business', 
        data =json.dumps(dict(businessname="Techbase", description="", category="laptops", location="runda")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
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
        print('hhijjmo',results)
        self.assertIn(results.content_type, 'application/json')

    def test_delete(self):
        """test API can delete business"""
        self.register_user()
        login = self.login_user()
        resp= json.loads(login.data.decode('UTF-8'))
        token = resp['token']
        new_buisness = self.app.post('/api/v1/business', 
        data =json.dumps(dict(businessname="Techbase", description="lala", category="laptops", location="runda")),
        headers={"Authorization":"Bearer {}".format(token)}, content_type="application/json")
        response=self.app.delete('/api/v1/business/0', 
        headers={"Authorization":"Bearer {}".format(token)}, content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Business successfully deleted", response_msg["message"])

