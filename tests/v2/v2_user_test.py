import json
import unittest
from database_tests import migrate, drop, create_admin
from app.apps import create_app

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        """make app testable"""
        self.client = self.app.test_client()
        with self.app.app_context():
            drop()
            migrate()
            create_admin()        

        self.admin_data ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'sylviawanjiku@gmail.com','password':"Admin!23!"}
        self.register_user_without_email ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'','password':D123456}
        self.register_user_without_firstname ={'username':'sylvia','first_name':'','last_name':'Mbugua','email':'spongebob@gmail.com','password':C123456}
        self.register_user_without_lastname ={'username':'sylvia','first_name':'Sylvie','last_name':'','email':'spongebob@gmail.com','password':B123456}
        self.register_user_without_username ={'username':'','first_name':'Sylvie','last_name':'','email':'spongebob@gmail.com','password':A123456}
        self.register_user ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'sylviawanjiku@gmail.com','password':"Admin!23!"}
        self.admin_login_data ={'email':'sylviawanjiku@gmail.com','password':"Admin!23!"}
        self.user_login_data ={'email':'spongebob@gmail.com','password':"123456!"}
        
    
    def test_register_user(self):
        '''Test API can create a new user (POST request)'''
        new_user = self.client.post('/api/v2/signup',data=json.dumps(self.register_user),content_type = 'application/json')       
        self.assertEqual(new_user.status_code, 201)

    def test_empty_email_registration(self):
        """Test for empty email"""
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_without_email),content_type = 'application/json')     
        result = json.loads(new_user.data.decode())
        self.assertEqual(new_user.status_code, 400)

    def test_register_user_empty_firstname(self):
        """Test for empty firstname"""
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_without_firstname),content_type = 'application/json')        
        result = json.loads(new_user.data.decode())
        self.assertEqual(new_user.status_code, 400)


    def test_register_user_empty_lastname(self):
        """Test for empty lastname"""
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_without_lastname),content_type = 'application/json')       
        result = json.loads(new_user.data.decode())
        self.assertEqual(new_user.status_code, 400)

    
    def test_register_user_empty_username(self):
        """Test for empty username"""
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.register_user_without_username),content_type = 'application/json')        
        result = json.loads(new_user.data.decode())
        self.assertEqual(new_user.status_code, 400)

    def test_admin_login(self):
        """Test method to login admin"""
        login_admin = self.client.post('/api/v2/signup',data = json.dumps(self.admin_login_data),content_type = 'application/json')        
        result = json.loads(login_admin.data.decode())
        self.assertEqual(login_admin.status_code, 400)

    def test_user_login(self):
        """Test method to login admin"""
        login_user = self.client.post('/api/v2/signup',data = json.dumps(self.user_login_data),content_type = 'application/json')        
        result = json.loads(login_user.data.decode())
        self.assertEqual(login_user.status_code, 400)

   