from flask import Flask, make_response, jsonify, request
from ...v2.models_v2.models import Product,Data_base ,Sales
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,get_jwt_identity)
from .authentication import admin_only
from functools import wraps
from .products import Single_Product


# request data validation
parser =reqparse.RequestParser()

parser.add_argument('attendant_name', required=True, help='attendant_name cannot be blank', type=str)
parser.add_argument('product_name', required=True, help='product_name cannot be blank', type=str)
parser.add_argument('quantity',required=True, help='quantity cannot be blank', type=int)
parser.add_argument('price',required=True, help='price cannot be blank',type = int)
parser.add_argument('total_price', required=True, help='total_price cannot be blank', type=int)

class Sale(Resource):
    @jwt_required
    def post(self):
        """Posting items to sales"""       
        args = parser.parse_args()
        attendant_name = args['attendant_name']
        product_name = args['product_name']
        quantity = args['quantity']
        price = args['price']
        total_price = args['total_price']

        product = Product().fetch_by_name(product_name)
        if not product:
            return {
            'message': 'Product not found'
            }, 404

        min_stock = Product().fetch_min_stock(product_name)


        price = Product().fetch_product_price(product_name)
        quantity = Product().fetch_product_quantity(product_name)
        print(min_stock)
        print(price)
        print(quantity)
        print(product)
 
