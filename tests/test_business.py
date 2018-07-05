import json
import datetime

from .base_test import BaseTestCase


class TestUsersTestcase(BaseTestCase):

    def test_register_business_without_token(self):
        """tests register without token"""
        response = self.business_registration_without_token()
        response_msg = json.loads(response.data.decode())
        self.assertIn("Token is required", response_msg['message'])

    def test_register_business_with_invalid_token(self):
        """tests empty with invalid token"""
        self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/businesses',
                                data=json.dumps(dict(businessname="Ramtoms",
                                                     description="sell iron boxes", category="electronics", location="juja")),
                                content_type="application/json",  headers={"Authorization": '99'})
        response = json.loads(resp.data.decode())
        self.assertIn("Invalid Token Please refresh", response['message'])

    def test_business_registration(self):
        """tests successful registration"""
        response = self.business_registration()
        response_msg = json.loads(response.data.decode())
        self.assertIn("Business successfully registered",
                      response_msg["message"])

    def test_returns_all_businesses(self):
        """test all businesses are returned"""
        response = self.business_registration()
        resp = self.client.get('/api/v1/businesses',
                               content_type="application/json")
        self.assertIn("Techbase", str(resp.data))

    def test_api_can_get_business_by_id(self):
        """get business by id"""
        response = self.business_registration()
        result = self.client.get('/api/v1/businesses/1',
                                 content_type="application/json")
        self.assertIn('we sell laptops', str(result.data))

    def test_get_by_ivalid_id(self):
        """tests if the id is not valid"""
        response = self.business_registration()
        result = self.client.get('/api/v1/businesses/2',
                                 content_type="application/json")
        self.assertIn("Business not found", str(result.data))

    def test_add_empty_business_name(self):
        """tests empty business name"""
        self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/businesses', data=json.dumps(
            self.business2), content_type="application/json", headers={"Authorization": token})
        response_msg = json.loads(response.data.decode())
        self.assertIn("businessname is required", response_msg['message'])

    def test_add_empty_business_category(self):
        """tests empty business category"""
        self.register_user()
        data = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/businesses', data=json.dumps(
            self.business3), content_type="application/json", headers={"Authorization": data})
        response_msg = json.loads(response.data.decode())
        self.assertIn("category is required", response_msg['message'])

    def test_add_empty_business_location(self):
        """tests empty business location"""
        self.register_user()
        data = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/businesses', data=json.dumps(
            self.business4), content_type="application/json", headers={"Authorization": data})
        response_msg = json.loads(response.data.decode())
        self.assertIn("description is required", response_msg['message'])

    def test_add_empty_business_description(self):
        self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/businesses', data=json.dumps(
            self.business5), content_type="application/json", headers={"Authorization": token})
        response_msg = json.loads(response.data.decode())
        self.assertIn("location is required", response_msg['message'])

    def test_business_can_be_edited(self):
        """tests if business posted can be edited"""
        self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/businesses',
                                data=json.dumps(self.business), content_type="application/json",  headers={"Authorization": token})

        response = self.client.put('/api/v1/businesses/1',
                                   data=json.dumps(dict(businessname="Ramtoms", description="sell col boxes", category="electronics", location="juja")), content_type="application/json",  headers={"Authorization": token})
        results = self.client.get('/api/v1/businesses/1',
                                  headers={"Authorization": token})

        self.assertIn("sell col boxes", str(results.data))

    def test_delete(self):
        """test API can delete business"""
        self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/businesses',
                                data=json.dumps(self.business), content_type="application/json",  headers={"Authorization": token})
        delete = self.client.delete(
            '/api/v1/businesses/1', headers={"Authorization": token})
        results = self.client.get('/api/v1/businesses/1')
        self.assertIn("Business not found", str(results.data))

    def test_delete_other_business(self):
        """tests if a user can delete others users business"""
        user1 = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/businesses', data=json.dumps(self.business),
                                    content_type="application/json", headers={"Authorization": token})
        self.person['email'] = 'muthash@gmail.com'
        user2 = self.register_user()
        token2 = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.delete('/api/v1/businesses/1', data=json.dumps(self.reviews),
                                  content_type="application/json", headers={"Authorization": token2})
        response_msg = json.loads(resp.data.decode())
        self.assertIn("You can only delete your business",
                      response_msg["message"])

    def test_delete_business_not_registered(self):
        """test API can delete business"""
        self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/businesses',
                                data=json.dumps(self.business), content_type="application/json",  headers={"Authorization": token})
        delete = self.client.delete(
            '/api/v1/business/2', headers={"Authorization": token})
        results = self.client.get('/api/v1/businesses/2')
        self.assertIn("Business not found", str(results.data))

    def test_search_business(self):
        """Test search business"""
        response = self.business_registration()
        results = self.client.get('/api/v1/businesses?search=T')
        self.assertIn("Techbase", str(results.data))
