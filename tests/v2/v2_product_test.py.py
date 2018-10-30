#  import sys
# import unittest
# import os
# import json
# from app.apps import create_app


# class TestProducts(unittest.TestCase):
        
#     def setUp(self):
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client()
#         self.products_data ={'product_id':'Sug001','product_name':'Sugar','brand':'Mumias','quantity':50,'price':500,'avail_stock':30,'min_stock':10,'uom':'kg','category':'kitchen'}

#      def test_new_product_creation(self):
#         """Test API can create a product (POST request)"""
#         token = self.get_token_as_admin()
#         self.post_product()
#         new_product = self.client.post('/api/v1/products',data = self.products_data)       
#         self.assertEqual(new_product.status_code, 201)
        