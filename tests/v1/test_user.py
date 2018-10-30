import sys
import unittest
import os
import json
from app.apps import create_app

class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        """make app testable"""
        self.client = self.app.test_client
        self.user_data ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'sylviawanjiku@gmail.com','password':234452}
        self.user_data_empty_email ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'','password':234452}
        self.user_data_empty_firstname ={'username':'sylvia','first_name':'','last_name':'Mbugua','email':'','password':234452}
        self.user_data_empty_lastname ={'username':'sylvia','first_name':'Sylvie','last_name':'','email':'','password':234452}
        self.user_data_empty_username ={'username':'','first_name':'Sylvie','last_name':'','email':'','password':234452}

    def test_register_user(self):
        '''Test API can create a new user (POST request)'''
        new_user = self.client().post('/api/v1/users',data = self.user_data)       
        self.assertEqual(new_user.status_code, 201)
    
    def test_register_user_empty_email(self):
        '''Test for empty email'''
        new_user = self.client().post('/api/v1/users',data = self.user_data_empty_email)       
        self.assertEqual(new_user.status_code, 400)

    def test_register_user_empty_firstname(self):
        '''Test for empty firstname'''
        new_user = self.client().post('/api/v1/users',data = self.user_data_empty_firstname)       
        self.assertEqual(new_user.status_code, 400)


    def test_register_user_empty_lastname(self):
        '''Test for empty lastname'''
        new_user = self.client().post('/api/v1/users',data = self.user_data_empty_lastname)       
        self.assertEqual(new_user.status_code, 400)

    
    def test_register_user_empty_username(self):
        '''Test for empty username'''
        new_user = self.client().post('/api/v1/users',data = self.user_data_empty_username)       
        self.assertEqual(new_user.status_code, 400)
