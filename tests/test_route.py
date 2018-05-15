# import json
# import unittest
# from source.routes.api import create_app, db


# class TestUsersTestcase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client
#         self.person={
#                 'username':'james muriuki',
#                 'email':'james20@yahoo.com',
#                 'password':'123456'
#                     }
#         self.person2={
#             'username':'james muriuki',
#             'password':'123456'
#                 }
#         self.person3 = {
#             'username':'james muriuki',
#             'email':'james',
#             'password':'123456'
#                 }

#         with self.app.app_context():
#             #create all tables
#             db.session.close()
#             db.drop_all()
#             db.create_all()


#     def test_users_registration_empty_username(self):
#         """tests if  username is empty"""
#         response=self.client().post('/api/auth/v1/register',data =json.dumps(dict(username="", email="jim@gamil.com", password="12345")), headers={'content-type':"application/json"})
#         self.assertEqual(response.status_code,401)
#         response_msg = json.loads(response.data.decode())
#         self.assertIn("Username is required",response_msg["message"])

#     def test_users_registration_empty_password(self):  
#         """tests if password is empty"""
#         response = self.client().post('/api/auth/v1/register', data =json.dumps(dict(username="james", email="jim@gamil.com", password="")), headers={'content-type':"application/json"})
#         response_msg = json.loads(response.data.decode("UTF-8"))
#         self.assertIn('Password is required',response_msg["message"])

#     def test_users_registration_empty_email(self):
#         """tests if email is empty"""        
#         response = self.client().post('/api/auth/v1/register', data =json.dumps(dict(username="james", email="", password="12345")), headers={'content-type':"application/json"})
#         response_msg = json.loads(response.data.decode("UTF-8"))
#         self.assertEqual(response.status_code,401)
#         self.assertIn("Email is required",response_msg["message"])

#     def test_users_registration_invalid_email(self):
#         """tests if email is invalid"""        
#         response = self.client().post('/api/auth/v1/register', data =json.dumps(self.person3), headers={'content-type':"application/json"})
#         self.assertEqual(response.status_code,401)
#         response_msg = json.loads(response.data.decode("UTF-8"))
#         self.assertIn("Email is invalid",response_msg["message"])

#     def test_users_registration_correct_registration(self):
#         """tests  correct login registration"""
#         response = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
#         self.assertEqual(response.status_code,201)
#         response_msg = json.loads(response.data.decode("UTF-8"))      
#         self.assertIn("User successfully registered", response_msg["Message"])
     
#     def test_login(self):
#         """returns correct login """
#         register = self.client().post('/api/auth/v1/register', data=json.dumps(self.person), headers={'content-type':"application/json"})
#         login= self.client().post('/api/v1/login', data=json.dumps(self.person2), headers={'content-type':"application/json"})
#         self.assertEqual(login.status_code,200)
#         data = json.loads(login.get_data())
#         self.assertIn('token',data)

#     def test_login_with_a_wrong_username(self):
#         """returns correct login """
#         register = self.client().post('/api/auth/v1/register', data=json.dumps(dict(username="james",email="james@gmail.com",password="12345")), headers={'content-type':"application/json"})
#         login= self.client().post('/api/v1/login', data=json.dumps(dict(username="jamesbond",password="12345")), headers={'content-type':"application/json"})
#         self.assertEqual(login.status_code, 404)
#         response_msg = json.loads(login.data.decode("UTF-8"))
#         self.assertIn("User not found",response_msg["message"])


#     def test_login_with_a_wrong_password(self):
#         """tests API if login Works With A wrong password"""
        
#         register = self.client().post('/api/auth/v1/register', data=json.dumps(dict(username="james",email="james@gmail.com",password="12345")), headers={'content-type':"application/json"})     
#         self.assertEqual(register.status_code,201)
#         login= self.client().post('/api/v1/login',data=json.dumps(dict(username="james",password="555")),content_type="application/json")
#         self.assertEqual(login.status_code, 401)
#         response_msg = json.loads(login.data.decode("UTF-8"))
#         self.assertIn("Wrong Password",response_msg["message"])


