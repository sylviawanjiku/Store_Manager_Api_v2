import unittest
import json
from app.apps import create_app
from database_tests import migrate, drop,create_admin 

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        """make app testable"""
        self.client = self.app.test_client()
        with self.app.app_context():
            drop()
            migrate()
            create_admin()

        
        self.user_data ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'sylviawanjiku@gmail.com','password':234452}
        self.user_data_empty_email ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'','password':234452}
        self.user_data_empty_firstname ={'username':'sylvia','first_name':'','last_name':'Mbugua','email':'','password':234452}
        self.user_data_empty_lastname ={'username':'sylvia','first_name':'Sylvie','last_name':'','email':'','password':234452}
        self.user_data_empty_username ={'username':'','first_name':'Sylvie','last_name':'','email':'','password':234452}


    def test_signup_user(self):
        '''Test API can create a new user (POST request)'''
        new_user = self.client.post('/api/v2/signup',data = json.dumps(self.user_data))   
        self.assertEqual(new_user.status_code, 201)

    

        