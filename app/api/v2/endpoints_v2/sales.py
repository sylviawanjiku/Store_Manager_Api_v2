from flask import Flask, make_response, jsonify, request
from ...v2.models_v2.models import Product,Data_base ,Sales
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,get_jwt_identity)
from .authentication import admin_only
from functools import wraps
from .products import Single_Product
from psycopg2 import extras,connect
import psycopg2

  # connect to the storemanager database
connect = psycopg2.connect(
    host="localhost",
    user= "postgres",
    password ="root",
    database ="Storemanager"
)
# request data validation
parser =reqparse.RequestParser()
cur = connect.cursor()

parser.add_argument('product_name', required=True, help='product_name cannot be blank', type=str)
parser.add_argument('quantity',required=True, help='quantity cannot be blank', type=int)

class Sale(Resource):
    @jwt_required
    def post(self):
        """Posting items to sales"""       
        args = parser.parse_args()
        product_name = args['product_name']
        quantity = args['quantity']
        
        attendant_name = get_jwt_identity()["username"]
        product = Product().fetch_by_name(product_name)
        if not product:
            return {
            'message': 'Product not found'
            }, 404
        min_stock = Product().fetch_min_stock(product_name)
        price = Product().fetch_product_price(product_name)
        available_quantity = Product().fetch_available_quantity(product_name)
        if quantity <= min_stock:
            return{"message":"Products running out of stock"}
        if quantity > available_quantity:
            return{"message":"Product is out of stock"}        
        available_quantity = available_quantity - quantity 

        cur.execute(
            """ UPDATE products SET avail_stock= %s WHERE product_name =%s""",(available_quantity,product_name))
        connect.commit()
       
        # if available_quantity <= min_stock:
        #     return{"message":"Products running out of stock"} 

        try:                         
            total_price = price * quantity
            """Add a sale to the created table products """
            insert_sale = "INSERT INTO sales(attendant_name,product_name,quantity,price,total_price) VALUES( %s, %s, %s, %s, %s)"
            sale_data = (attendant_name, product_name, quantity ,price ,total_price)
            cur.execute(insert_sale,sale_data)
            connect.commit()
            return {'message':'Sale successful',"remaining quantity": available_quantity},201
        
        except Exception as e:
            print(e)
            return {'message':'Internal server error'},500


class Get_Sales_Admin(Resource):
    @jwt_required
    @admin_only
    def get(self):
        """Get all sales"""
        sales_list = Sales().fetch_all_sales()
        if not sales_list:
            return {
            'message': 'The sales list is empty'
            }, 200       
        return {"message":"success","sales": sales_list},200

class Get_Sales_Attendant(Resource):
    @jwt_required
    def get(self,attendant_name):
        """Get all sales"""
        sales_list = Sales().fetch_all_sales_attendant_name(attendant_name)
        if not sales_list:
            return {
            'message': 'The sales list is empty'
            }, 200       
        return {"message":"success","sales": sales_list},200

       