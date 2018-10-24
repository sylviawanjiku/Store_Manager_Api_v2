from flask import Flask, make_response, jsonify, request
from ..models.product_model import Product
from ..models.sales_model import Sale
from flask_restful import Resource, reqparse
from datetime import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity,get_raw_jwt)


# request data validation
parser =reqparse.RequestParser()

parser.add_argument('sale_record_id', required=True, help='sale_record_id cannot be blank', type=str)
parser.add_argument('user_id', required=True, help='user_id cannot be blank', type=str)
parser.add_argument('username',required=True, help='username cannot be blank',type = str)
parser.add_argument('cart_id', required=True, help='cart_id cannot be blank', type=int)
parser.add_argument('sale_date',required=True, help='Username cannot be blank', type=datetime)
parser.add_argument('total',required=True, help='total cannot be blank', type =int)

class SalesRecord(Resource):
    def post(self):
        '''Posting items to sales'''        
        args = parser.parse_args()

        sale_record_id = args['sale_record_id']
        user_id = args['user_id']
        username = args['username']
        cart_id = args['cart_id']
        sale_date = args['sale_date']
        total =args['total'] 

        try:
            my_new_sale = Sale(sale_record_id,user_id,username,cart_id,sale_date,total)
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
