import unittest
import json
from app.apps import create_app


        
class BaseTest(unittest.TestCase):
        
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.products_data ={'product_id':'Sug001','product_name':'Sugar','brand':'Mumias','quantity':50,'price':500,'avail_stock':30,'min_stock':10,'uom':'kg','category':'kitchen'}
        self.admin_login ={'email':'sylviawanjiku@gmail.com','password':"Admin!23!"}
        
    def user_signup(self):
        reg_res =self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_data))   
        return reg_res

    def user_login(self):
        log_res =self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))   
        return log_res