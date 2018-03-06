from source.api import app
from unittest import TestCase
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.business = {
            "id":1,
            "businessname":"Techbase",
            "description":"we sell laptops",
            "category":"electronics",
            "location":"River road"
                        }
    def teardown(self):
        del self.business
        pass

    def test_business_registration(self):
        #test business successfully is registered 
        response=self.app.post('http://127.0.0.1:5000/api/auth/v1/business', data=self.business)
        self.assertEqual(response.status_code,200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business successfully registered", response_msg["Message"]) 

    def test_returns_all_businesses(self):
        #test all businesses are returned
        response=self.app.post('http://127.0.0.1:5000/api/auth/v1/business', data=self.business)
        self.assertEqual(response.status_code,201)
        response = self.app.get('http://127.0.0.1:5000/api/auth/v1/business')
        self.assertIn('we sell laptops', str(response.data))

    def test_api_can_get_business_by_id(self):
        #get business by id
        response = self.app.post('http://127.0.0.1:5000/api/auth/v1/business',data=self.business)
        self.assertEqual(response.status_code,201)
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        result = self.app.get('http://127.0.0.1:5000/api/auth/v1/business/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code,200)
        self.assertIn('we sell laptops', str(result.data))

    def test_get_bad _request(self):
        #test if bad request is passed
        response=self.app.get('http://127.0.0.1:5000/api/auth/v1/business/biz')
        self.assertEqual(result.status.code,400)

    def get_by_ivalid_id(self):
        #tests if the id is not valid
        response=self.app.get('http://127.0.0.1:5000/api/auth/v1/business/4')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("Business not found", response_msg["Message"])

    def test_add_empty_business_name(self):
        reponse=self.app.post('http://127.0.0.1:5000/api/auth/v1/business/biz', data=dict(businessname=""))
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business name cannot be empty", response_msg['Message'])


#make tests run
if __name__ == "__main__":
   unittest.main()



