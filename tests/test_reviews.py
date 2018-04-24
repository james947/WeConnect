from base import BaseTestCase
import json


class TestIntegrations(BaseTestCase):
    """tests for reviews endpoints"""
    def test_add_new_review(self):
        """Api creates a new review"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register = self.app.post('/api/v1/business', 
        data=json.dumps(dict(businessname="techbase", description="yoyo", category="blabla", location="runda")),  
        content_type="application/json", headers={"Authorization":"Bearer {}".format(token)})
        response = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(dict(title="app", description="yoyo")), 
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Review Added Successfully", response_msg["message"]) 

    def test_add_empty_review_title(self):
        """"tests_ if review_title is empty"""
        self.login_user()
        self.register_user()
        self.business_registration()
        response = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(dict(title="", description="Your app is great")), 
        content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Title is required", response_msg["message"]) 

    def test_add_empty_review_description(self):
        """"tests if review_description is empty"""
        self.login_user()
        self.register_user()
        self.business_registration()
        response = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(dict(title="app",description="")), 
        content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Description is required", response_msg["message"]) 

    def test_get_review(self):
        """Test if APi gets review."""
        self.register_user()
        login = self.login_user()
        resp  = json.loads(login.data.decode())
        token = resp['token']
        register = self.app.post('/api/v1/business', 
        data=json.dumps(dict(businessname="techbase", description="yoyo", category="blabla", location="runda")),  
        content_type="application/json", headers={"Authorization":"Bearer {}".format(token)})
        review = self.app.post('/api/v1/business/0/review', 
        data=json.dumps(dict(title="app", description="yoyo")), 
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        get_review = self.app.get('/api/v1/business/0/review', 
        data=json.dumps(dict(title="app", description="yoyo")), content_type="application/json")
        response_msg = json.loads(get_review.data.decode("utf-8"))
        print(response_msg)
        self.assertIn("yoyo", response_msg.data) 




    

    