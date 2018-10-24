from flask import Flask, make_response, jsonify, request
from ..models.product_model import Product
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity,get_raw_jwt)


# request data validation
parser =reqparse.RequestParser()
parser.add_argument('product_id',required=True, help='product_id cannot be blank',type =int)
parser.add_argument('product_name',required=True, help='product_name cannot be blank',type =str)
parser.add_argument('brand',required=True, help='brand cannot be blank',type =str)
parser.add_argument('quantity',required=True, help='quantity cannot be blank',type = int)
parser.add_argument('price',required=True, help='price cannot be blank', type =int)
parser.add_argument('avail_stock',required=True, help='avail_stock cannot be blank',type =int)
parser.add_argument('min_stock',required=True, help='min_stock cannot be blank',type =int)
parser.add_argument('uom',required=True, help='uom cannot be blank',type =str)
parser.add_argument('category',required=True, help='category cannot be blank',type =str)


class Products(Resource):
    def get(self,product_id = None):
        # Get all products in the list
        if product_id is None:
            product = Product.get_products(self)
            # If the list is empty
            if len(product) == 0:
                return make_response(jsonify({
                'message': 'The product list is empty'
                }), 200)
            return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'success',
                    'product': product
                }
            ), 200)
        '''Get a single product from the products list'''
        view_product = Product.get_single_product(self,product_id)
        if view_product:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'product': view_product
            }), 200)

        '''Identify a single item with it's id and fetch it and if it's not present return the following '''   
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)

       
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
            new_product = my_product.post_product()
            
            return make_response(jsonify({
                    'product': new_product
                }), 201)

        except Exception as e:
            print(e)
            return{'message':'Internal server error'},500
