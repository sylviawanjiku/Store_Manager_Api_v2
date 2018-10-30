import sys
import unittest
import os
import json
from app.apps import create_app


class TestSales(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(config_name="testing")
        """make app testable"""
        self.client = self.app.test_client
        self.sales_data ={'sale_id':'sl001','product_name':'Sugar','brand':'Mumias','quantity':50,'price':500,'sale_date' :'24/04/2018','no_of_items': 24,'total':500}

    
    def test_new_sale_creation(self):
        '''Test API can create a sale record (POST request)'''
        new_sale = self.client().post('/api/v1/sales',data = self.sales_data)       
        self.assertEqual(new_sale.status_code, 201)
    
    def test_api_can_get_all_sales(self):
        '''Test API can get sales record (GET request)'''
        added_sale = self.client().post('/api/v1/sales',data = self.sales_data)
        self.assertEqual(added_sale.status_code, 201)
        res = self.client().get('/api/v1/sales')
        self.assertEqual(res.status_code, 200)
    def test_api_can_get_a_single_sale(self):
        '''Test API can get a single sale record (GET<id> request).'''
        added_sale = self.client().post('/api/v1/sales',data = self.sales_data)
        self.assertEqual(added_sale.status_code, 201)
        added_sale_id = json.loads(added_sale.data.decode())

        ''' Check for posted sale and fetch the sale verify if the sales data is correct'''
        posted_sale_data = self.client().get('/api/v1/sales/{}'.format(added_sale_id['sale'] ['id']))
        self.assertEqual(posted_sale_data.status_code, 200)
        
    """make the test executable"""
if __name__=='__main__':
    unittest.main()
