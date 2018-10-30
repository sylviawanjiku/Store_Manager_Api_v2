from flask import Flask, make_response, jsonify, request
from ..models.product_model import Product
from ..models.sales_model import Sale
from flask_restful import Resource, reqparse
from datetime import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity,get_raw_jwt)


# request data validation
parser =reqparse.RequestParser()

parser.add_argument('attendant_name', required=True, help='attendant_name cannot be blank', type=str)
parser.add_argument('product_name', required=True, help='product_name cannot be blank', type=str)
parser.add_argument('price',required=True, help='price cannot be blank',type = int)
parser.add_argument('total_price', required=True, help='total_price cannot be blank', type=int)
parser.add_argument('quantity',required=True, help='quantity cannot be blank', type=int)


class SalesRecord(Resource):
    def post(self):
        '''Posting items to sales'''        
        args = parser.parse_args()

        attendant_name = args['attendant_name']
        product_name = args['product_name']
        price = args['price']
        total_price = args['total_price']
        quantity = args['quantity']
        product_list=Product.products
        product =[product for product in product_list if product['product_name']==product_name]
        if not product:
            return {"message":"Product does not exist"}
        product[0]['quantity']= product[0]['quantity'] - quantity
        if product[0]['quantity']<0:
            return{"message":"Product is out of stock"}
        try:
            my_new_sale = Sale(attendant_name,product_name,price,total_price,quantity)
            new_sale = my_new_sale.post_sale()
            return make_response(jsonify({
                    'sale': new_sale
                }), 201)

        except Exception as e:
            print(e)
            return{'message':'Internal server error'},500

   
    def get(self,sale_id = None):
        # Get all sales in the list
        if sale_id is None:
            sale = Sale.get_sales(self)
            # If the list is empty
            if len(sale) == 0:
                return make_response(jsonify({
                'message': 'The sales record list is empty'
                }), 200)
            return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'success',
                    'sale': sale
                }
            ), 200) 
            
        """Get a single sale from the sales list"""
        view_sale = Sale.get_single_sale(self,sale_id)
        if view_sale:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'sale': view_sale
            }), 200)

        '''Identify a single item with it's id and fetch it and if it's not present return the following '''   
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)      
