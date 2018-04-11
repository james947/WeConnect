import json
import unittest
from source.routes.api import create_app, db
from source.routes.auth import views

class TestUsersTestcase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
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
        self.business3 = {
            "businessname": "Techbase",
            "description": "we sell laptops",
            "category": "",
            "location": "River road"
        }

        self.business4 = {
            "businessname": "Techbase",
            "description": "we sell laptops",
            "category": "electronics",
            "location": ""
        }

        self.business5 = {
            "businessname": "Techbase",
            "description": "",
            "category": "electronics",
            "location": "River road"
        }

        self.person={
                'username':'james',
                'email':'james20@yahoo.com',
                'password':'123456'
                    }


        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    
    def test_register_business_without_token(self):
        # tests empty token
        response = self.client().post('/api/v1/business',
                                data=dict(businessname="techbase", description="we sell laptops", category="", location="juja"))
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Token is required", response_msg['message'])

    def test_register_business_with_invalid_token(self):
        """tests empty with invalid token"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business2), content_type="application/json", headers={"x-access-token":'tokne'})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("Token is invalid!", response_msg['message'])


    def test_business_registration(self):
        """tests successful registration"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business), content_type="application/json", headers={"x-access-token":token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode())
        self.assertIn("Business successfully registered", response_msg["message"])

    def test_returns_all_businesses(self):
        """test all businesses are returned"""

        register = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james", password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business), content_type="application/json", headers={"x-access-token":token})
        resp = self.client().get('/api/v1/business', headers={"x-access-token":token})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Techbase", str(resp.data))

    def test_api_can_get_business_by_id(self):
        """get business by id"""
        register = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james", password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        resp = self.client().post('/api/v1/business', data=json.dumps(self.business), content_type="application/json", headers={"x-access-token":token})
        result = self.client().get('/api/v1/business/1', headers={"x-access-token":token})
        self.assertEqual(result.status_code, 200)
        self.assertIn('we sell laptops', str(result.data))

    def test_get_by_ivalid_id(self):
        """
        tests if the id is not valid``
        """
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        register = self.client().post('/api/v/business', data=self.business, content_type="application/json", headers={"x-access-token":token})
        response = self.client().get('/api/v1/business/4', headers={"x-access-token":token})
        response_msg = json.loads(response.data)
        self.assertIn("Business not found", response_msg["message"])

    def test_add_empty_business_name(self):
        """tests empty business name"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business2), content_type="application/json", headers={"x-access-token":token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("Businessname required", response_msg['message'])

    def test_add_empty_business_category(self):
        """tests empty business category"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business3), content_type="application/json", headers={"x-access-token":token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("Category name required", response_msg['message'])

    def test_add_empty_business_location(self):
        """tests empty business location"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business4), content_type="application/json", headers={"x-access-token":token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("Location name required", response_msg['message'])

    def test_add_empty_business_description(self):
        """tests empty business location"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business5), content_type="application/json", headers={"x-access-token":token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode())
        print(response_msg)
        self.assertIn("Description is  required", response_msg['message'])

    def test_business_can_be_edited(self):
        """
        tests if business posted can be edited
        """
        resp = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        resp_1 = self.client().post('/api/v1/business',
                                 data=json.dumps(self.business), content_type="application/json",  headers={"x-access-token":token})                       
        response = self.client().put('/api/v1/business/1',
                                data=json.dumps(dict(businessname="Ramtoms", description="sell iron boxes", category="electronics", location="juja")), content_type="application/json",  headers={"x-access-token":token})
        self.assertEqual(response.status_code, 200)
        results = self.client().get('/api/v1/business/1', headers={"x-access-token":token})
        self.assertIn("sell iron boxes", str(results.data))

    def test_delete(self):
        """test API can delete business"""
        response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
        login = self.client().post('/api/v1/login', data=json.dumps(dict(username="james",password="123456")), content_type="application/json")
        data = json.loads(login.data.decode("UTF-8"))
        token = data['token']
        response = self.client().post('/api/v1/business', data=json.dumps(self.business), content_type="application/json", headers={"x-access-token":token})
        self.assertEqual(response.status_code, 201)
        delete = self.client().delete('/api/v1/business/1', headers={"x-access-token":token})
        response = self.assertEqual(delete.status_code, 202)
        # tests to see if business exists
        response = self.client().get('/api/v1/business/1',  headers={"x-access-token":token})
        self.assertEqual(response.status_code, 404)



