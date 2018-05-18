import json
from .base_test import BaseTestCase


class TestUsersTestcase(BaseTestCase):

    def test_add_new_review(self):
        """Api creates a new review"""
        user1 = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/business', data=json.dumps(self.business),
                                      content_type="application/json", headers={"x-access-token": token})
        self.person['email'] = 'muthash@gmail.com'
        user2 = self.register_user()
        token2 = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/business/1/reviews', data=json.dumps(self.reviews),
                                  content_type="application/json", headers={"x-access-token": token2})
        response_msg = json.loads(resp.data.decode())
        self.assertIn("Review Added Successfully", response_msg["message"])

    def test_add_null_review_title(self):
        """testsif review title is empty"""
        user1 = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/business', data=json.dumps(self.business),
                                      content_type="application/json", headers={"x-access-token": token})
        self.person['email'] = 'muthash@gmail.com'
        user2 = self.register_user()
        token2 = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/business/1/reviews', data=json.dumps(self.reviews2),
                                  content_type="application/json", headers={"x-access-token": token2})
        response_msg = json.loads(resp.data.decode())
        self.assertIn("title is required", response_msg["message"])

    def test_add_null_review_description(self):
        """"
        tests APi result if preview title is null
        """
        user1 = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/business', data=json.dumps(self.business),
                                      content_type="application/json", headers={"x-access-token": token})
        self.person['email'] = 'muthash@gmail.com'
        user2 = self.register_user()
        token2 = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/business/1/reviews', data=json.dumps(self.reviews3),
                                  content_type="application/json", headers={"x-access-token": token2})
        response_msg = json.loads(resp.data.decode())
        self.assertIn("review is required", response_msg["message"])

    def test_get_review(self):
        """Test if APi gets review"""
        user1 = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/business', data=json.dumps(self.business),
                                      content_type="application/json", headers={"x-access-token": token})
        self.person['email'] = 'muthash@gmail.com'
        user2 = self.register_user()
        token2 = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/business/1/reviews', data=json.dumps(self.reviews),
                                  content_type="application/json", headers={"x-access-token": token2})
        review = self.client.get('/api/v1/business/1/reviews')
        self.assertEqual(review.status_code, 200)

    def test_get_invalid_review(self):
        """Tests Api when request is invalid"""
        user1 = self.business_registration()
        resp = self.client.get('/api/v1/business/1/reviews')
        response_msg = json.loads(resp.data.decode())
        self.assertEqual('Reviews not found', response_msg['message'])

    def test_review_own_business(self):
        reg = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/business', data=json.dumps(self.business),
                            content_type="application/json", headers={"x-access-token": token})
        resp = self.client.post('/api/v1/business/1/reviews', data=json.dumps(self.reviews),
                            content_type="application/json", headers={"x-access-token": token})
        response_msg = json.loads(resp.data.decode())
        self.assertEqual('You cannot review your Business', response_msg['message'])


    def test_review_business_not_registered(self):
        reg = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.post('/api/v1/business/1/reviews', data=json.dumps(self.reviews),
                            content_type="application/json", headers={"x-access-token": token})
        response_msg = json.loads(resp.data.decode())
        self.assertEqual('Business not found', response_msg['message'])
    
    def test_get_all_reviews_for_business_not_registered(self):
        reg = self.register_user()
        token = json.loads(self.login_user().data.decode("UTF-8"))['token']
        resp = self.client.get('/api/v1/business/1/reviews', data=json.dumps(self.reviews),
                            content_type="application/json", headers={"x-access-token": token})
        response_msg = json.loads(resp.data.decode())
        self.assertEqual('Business not found', response_msg['message'])




    