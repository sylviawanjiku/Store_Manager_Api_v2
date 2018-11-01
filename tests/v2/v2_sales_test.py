import sys
import unittest
import os
import json
from app.apps import create_app


class TestSales(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(config_name="testing")
        """make app testable"""
        self.client = self.app.test_client()
        self.products_data ={'product_id':'Sug001','product_name':'Sugar','brand':'Mumias','quantity':50,'price':500,'avail_stock':30,'min_stock':10,'uom':'kg','category':'kitchen'}
        self.sales_data ={'product_name':'Sugar','quantity':'10'}
        self.admin_login ={'email':'sylviawanjiku@gmail.com','password':"Admin!23"}
        self.user_data ={'username':'sylvia','first_name':'Sylvie','last_name':'Mbugua','email':'mbuguasly@gmail.com','password':'QR234452','is_admin':'False'}
        self.user_login ={'email':'mbuguasly@gmail.com','password':'QR234452'}
        self.admin_data ={'username':'SylviaW','first_name':'Sylvie','last_name':'Mbugua','email':'sylviawanjiku@gmail.com','password':'Admin!23','is_admin':'True'}

    
    def test_new_sale_creation(self):
        '''Test API can create a sale record (POST request)'''
        reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.user_data))
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Product added successfully")
        self.assertEqual(post_product.status_code,201)
        
        make_sale =self.client.post('/api/v2/sales',data=json.dumps(self.sales_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
        res = json.loads(make_sale.data.decode())
        self.assertEqual(res['message'],  "Sale successful")
        self.assertEqual(make_sale.status_code,201)

    def test_admin_can_get_all_sales(self):
        """Test API can create a sale record (POST request)"""
        reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.admin_data))
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Product added successfully")
        self.assertEqual(post_product.status_code,201)
        
        make_sale =self.client.post('/api/v2/sales',data=json.dumps(self.sales_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
        res = json.loads(make_sale.data.decode())
        self.assertEqual(res['message'],  "Sale successful")
        self.assertEqual(make_sale.status_code,201)

        get_all_sales =self.client.post('/api/v2/sales/',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res_prod = json.loads(get_all_sales.data.decode())
        self.assertEqual(res_prod['message'],  "sales successfully retrieved")
        self.assertEqual(get_all_sales.status_code,200)
    
    # def test_attendant_can_get_personal_sales(self):
    #     '''Test API can create a sale record (POST request)'''
    #     reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.user_data))
    #     login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_login))
    #     created_token = json.loads(login.data.decode())["access_token"]
    #     post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
    #     res = json.loads(post_product.data.decode())
    #     self.assertEqual(res['message'],  "Product added successfully")
    #     self.assertEqual(post_product.status_code,201)
        
    #     make_sale =self.client.post('/api/v2/sales',data=json.dumps(self.sales_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
    #     res = json.loads(make_sale.data.decode())
    #     self.assertEqual(res['message'],  "Sale successful")
    #     self.assertEqual(make_sale.status_code,201)

if __name__=='__main__':
        unittest.main()
