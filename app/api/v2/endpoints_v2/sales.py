from flask import Flask, make_response, jsonify, request
from ...v2.models_v2.models import Product,Data_base ,Sales
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,get_jwt_identity)
from .authentication import admin_only
from functools import wraps
from .products import Single_Product


# request data validation
parser =reqparse.RequestParser()

parser.add_argument('product_name', required=True, help='product_name cannot be blank', type=str)
parser.add_argument('quantity',required=True, help='quantity cannot be blank', type=int)

class Sale(Resource):
    @jwt_required
    def post(self):
        """Posting items to sales"""       
        args = parser.parse_args()
        product_name = args['product_name']
        quantity = args['quantity']
        
        attendant_name = get_jwt_identity()
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
       
        # product[0]['quantity']= product[0]['quantity'] - quantity
        # if product[0]['quantity']<0:
        #     return{"message":"Product is out of stock"}
        available_quantity = available_quantity - quantity 
        if available_quantity <= min_stock:
            return{"message":"Products running out of stock"}
        if available_quantity < quantity:
             return{"message":"Cannot make sale"}
        try:                         
            total_price = price * quantity
            my_new_sale = Sales(attendant_name,product_name,quantity,price,total_price)
            my_new_sale.add()
            return{"message":"Sale added successfully", "sale": my_new_sale.serialize()}, 201
        
        except Exception as e:
            print(e)
            return {'message':'Internal server error'},500

       