from flask import Flask, make_response, jsonify, request
from ..models_v2.models import Product ,Data_base
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,get_jwt_identity)
from .authentication import admin_only
from functools import wraps

# request data validation
parser =reqparse.RequestParser()
parser.add_argument('product_id',required=True, help='product_id cannot be blank',type =str)
parser.add_argument('product_name',required=True, help='product_name cannot be blank',type =str)
parser.add_argument('brand',required=True, help='brand cannot be blank',type =str)
parser.add_argument('quantity',required=True, help='quantity cannot be blank',type = int)
parser.add_argument('price',required=True, help='price cannot be blank', type =int)
parser.add_argument('avail_stock',required=True, help='avail_stock cannot be blank',type =int)
parser.add_argument('min_stock',required=True, help='min_stock cannot be blank',type =int)
parser.add_argument('uom',required=True, help='uom cannot be blank',type =str)
parser.add_argument('category',required=True, help='category cannot be blank',type =str)


class Products(Resource):
    @jwt_required
    @admin_only
    def post(self):
        '''Posting items to products'''        
        args = parser.parse_args()
        product_id = args['product_id']
        product_name = args['product_name']
        brand = args['brand']
        quantity = args['quantity']
        price = args['price']
        avail_stock = args['avail_stock']
        min_stock =args['min_stock']
        uom =args['uom']
        category = args['category']  

              
        try:
            my_product = Product(product_id,product_name,brand,quantity,price,avail_stock,min_stock,uom,category)
            my_product.add()

            return{"message":"Product added successfully", "product": my_product.serialize()}, 201

        except Exception as e:
            print(e)
            return{'message':'Internal server error'},500

    @jwt_required
    @admin_only
    def get(self):
        """Get all products"""
        products_list = Product().fetch_all_products()
        if not products_list:
             return make_response(jsonify)({
            'message': 'The product list is empty'
            }, 200) 
        return {"message":"success","products":[product.serialize() for product in products_list]},200
        
    # @jwt_required
    # @admin_only
    # def get_single_product(self,product_id):
    #     """Get single product"""
    #     product = Product().fetch_by_id(product_id)
    #     if not product:
    #          return make_response(jsonify)({
    #         'message': 'Product not found'
    #         }, 404) 
    #     return {"message":"success","product":product.serialize()},200
        