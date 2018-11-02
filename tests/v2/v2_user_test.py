
import json
import os
import unittest
import sys
from database_tests import migrate, drop, create_admin
from app.apps import create_app


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        """make app testable"""
        self.admin_data ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'sylviawanjiku@gmail.com','password':"Admin!23!",'is_admin':'True'}
        self.admin_login ={'email':'sylviawanjiku@gmail.com','password':"Admin!23!"}
        self.user_data={'spongebob':'sylvia','first_name':'Sponge','last_name':'Bob','email':'spongebob@gmail.com','password':"A123456",'is_admin':'False'}
        self.user_login={'email':'spongebob@gmail.com','password':"A123456"}
        self.register_user_without_valid_email ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'sylviambuguagmail.com','password':"D123456",'is_admin':'False'}
        self.register_user_with_invalid_firstname ={'username':'11 11','first_name':'','last_name':'Mbugua','email':'spongebob@gmail.com','password':"C123456",'is_admin':'False'}
        self.register_user_with_invalid_lastname ={'username':'sylvia','first_name':'Sylvie','last_name':'11 22','email':'spongebob@gmail.com','password':"B123456",'is_admin':'False'}
        self.register_user_with_invalid_username ={'username':'556','first_name':'Sylvie','last_name':'','email':'spongebob@gmail.com','password':"A123456",'is_admin': 'False'}
        self.register_user_with_invalid_password ={'username':'556','first_name':'Sylvie','last_name':'','email':'spongebob@gmail.com','password':"5  6",'is_admin': 'False'}
       
    def test_admin_login(self):
        """Test method to login admin"""
        login_admin = self.client.post('/api/v2/login',data = json.dumps(self.admin_login),content_type = 'application/json')        
        result = json.loads(login_admin.data.decode())
        self.assertEqual(result['message'], "User successfully logged In")
        self.assertEqual(login_admin.status_code, 200)

    def test_user_login(self):
        """Test method to login user"""
        login_user = self.client.post('/api/v2/login',data = json.dumps(self.user_login),content_type = 'application/json')        
        result = json.loads(login_user.data.decode())
        self.assertEqual(result['message'], "User successfully logged In")
        self.assertEqual(login_user.status_code, 200)   
            
    def test_register_user(self):
        '''Test API can create a new user (POST request)'''
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["token"]
        new_user = self.client.post('/api/v2/signup',data=json.dumps(self.user_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))    
        response = json.loads(new_user.data.decode())
        self.assertEqual(response['message'], "user created successfully")
        self.assertEqual(new_user.status_code, 201)
        

    def test_user_with_invalid_email_registration(self):
        """Test for invalid email"""
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["token"]
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_without_valid_email),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))     
        result = json.loads(new_user.data.decode())
        self.assertEqual(result ['message'], "enter valid email")
        self.assertEqual(new_user.status_code, 400)
       

    def test_register_user_with_invalid_firstname(self):
        """Test for invalid firstname"""
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["token"]
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_with_invalid_firstname),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))     
        result = json.loads(new_user.data.decode())
        self.assertEqual(result ['message'], "username must be a string")
        self.assertEqual(new_user.status_code, 400)
       
       


    def test_register_user_with_invalid_lastname(self):
        """Test for invalid lastname"""
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["token"]
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_with_invalid_lastname),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))     
        result = json.loads(new_user.data.decode())
        self.assertEqual(result ['message'], "Lastname must be a string")
        self.assertEqual(new_user.status_code, 400)


    def test_register_user_with_invalid_username(self):
        """Test for empty username"""
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["token"]
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_with_invalid_username),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))         
        result = json.loads(new_user.data.decode())
        self.assertEqual(result ['message'], "username must be a string")
        self.assertEqual(new_user.status_code, 400)

 
    def test_register_user_with_invalid_password(self):
        """Test for invalid password"""
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["token"]
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_with_invalid_password),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))         
        result = json.loads(new_user.data.decode())
        self.assertEqual(result ['message'], "Password should start with a capital letter and include a number")
        self.assertEqual(new_user.status_code, 400)
    
    if __name__=='__main__':
        unittest.main()

