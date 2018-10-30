"""
This module defines the sale model and associated functions
"""
from datetime import datetime, timedelta

class Sale():
    sales = []
    def __init__(self,attendant_name,product_name,price,total_price,quantity):
        """Instanciate the variables for my methods"""
        self.attendant_name =attendant_name 
        self.product_name = product_name
        self.price =price
        self.total_price =total_price
        self.quantity = quantity 

    def post_sale(self):
        sale_data=dict(
            id = len(Sale.sales),
            attendant_name = self.attendant_name,
            product_name = self.product_name,
            price = self.price,
            total_price =self.total_price,
            quantity =self.quantity, 
        )
        self.sales.append(sale_data)
        return(sale_data)

    def get_sales(self):
        # fetch all sales
        return  Sale.sales
        
    def get_single_sale(self,sale_id):
        single_sale= [sale for sale in Sale.sales if int(sale['id']) == int(sale_id)]
        if single_sale:
            return single_sale
