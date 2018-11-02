import sys
import unittest
import os
import json
from app.apps import create_app


        
class TestProducts(unittest.TestCase):
        
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.products_data = {'product_id': 'Sug001',
                              'product_name': 'Sugar',
                              'brand': 'Mumias',
                              'quantity': "50",
                              'price': "500",
                              'avail_stock': "30",
                              'min_stock': "10",
                              'uom': 'kg',
                              'category': 'kitchen'}
        self.admin_login = {'email': 'sylviawanjiku@gmail.com',
                            'password': "Admin!23"}
        self.user_data = {'username': 'sylvia',
                          'first_name': 'Sylvie',
                          'last_name': 'Mbugua',
                          'email': 'mbuguasly@gmail.com',
                          'password': 'QR234452',
                          'is_admin': 'False'}
        self.user_login = {'email': 'mbuguasly@gmail.com',
                           'password': 'QR234452'}
        self.admin_data = {'username': 'SylviaW',
                           'first_name': 'Sylvie',
                           'last_name': 'Mbugua',
                           'email': 'sylviawanjiku@gmail.com',
                           'password': 'Admin!23',
                           'is_admin': 'True'}

    def test_new_product_creation(self):
        """Test API can create a product (POST request)"""

        reg = self.client.post("api/v2/signup", content_type='application/json',
                               data=json.dumps(self.admin_data))
        login = self.client.post("api/v2/login", 
                                content_type='application/json',
                                 data=json.dumps(self.admin_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Product added successfully")
        self.assertEqual(post_product.status_code,201)
        
    def test_new_product_creation_admin_only(self):
        """Test API can create a product (POST request)"""

        reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.user_data))
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Invalid token ,unauthorized access ")
        self.assertEqual(post_product.status_code,401)

    def test_api_can_get_all_products(self):
        reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.user_data))
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Product added successfully")
        self.assertEqual(post_product.status_code,201)

        get_all_product =self.client.post('/api/v2/products/',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res_prod = json.loads(post_product.data.decode())
        self.assertEqual(res_prod['message'],  "Products retrieved successfully")
        self.assertEqual(get_all_product.status_code,200)
        

    def test_api_can_get_a_single_product(self):
        """Test API can get a single product (GET<id> request)."""
        reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.user_data))
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Product added successfully")
        self.assertEqual(post_product.status_code,201)

        get_single_product =self.client.post('/api/v2/products/{}'.format(post_product['product'] ['id']),data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res_prod = json.loads(get_single_product.data.decode())
        self.assertEqual(res_prod['message'],  "Product retrieved successfully")
        self.assertEqual(get_single_product.status_code,200)

    def test_api_can_update_a_single_product(self):
        """Test API can get a single product (GET<id> request)."""
        reg = self.client.post("api/v2/signup",content_type = 'application/json',data = json.dumps(self.user_data))
        login = self.client.post("api/v2/login",content_type = 'application/json',data = json.dumps(self.user_login))
        created_token = json.loads(login.data.decode())["access_token"]
        post_product =self.client.post('/api/v2/products',data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res = json.loads(post_product.data.decode())
        self.assertEqual(res['message'],  "Product added successfully")
        self.assertEqual(post_product.status_code,201)

        get_single_product =self.client.post('/api/v2/products/{}'.format(post_product['product'] ['id']),data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res_prod = json.loads(get_single_product.data.decode())
        self.assertEqual(res_prod['message'],  "Product retrieved successfully")
        self.assertEqual(get_single_product.status_code,200)

        update_single_product =get_single_product =self.client.post('/api/v2/products/{}'.format(post_product['product'] ['id']),data=json.dumps(self.products_data),content_type = 'application/json',headers =dict(Authorization = "Bearer{}".format(created_token)))  
        res_udate_prod = json.loads(update_single_product.data.decode())
        self.assertEqual(res_udate_prod['message'],  "Product retrieved successfully")
        self.assertEqual(update_single_product.status_code,200)

if __name__=='__main__':
    unittest.main()
