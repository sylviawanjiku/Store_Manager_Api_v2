from flask_restful import Api
from flask import Blueprint
from .endpoints_v2.products import  Products,Single_Product,Update_Product
from .endpoints_v2.user import SignUp
from .endpoints_v2.authentication import Login



version2 = Blueprint ('api_v2',__name__, url_prefix='/api/v2')

api_v2 = Api(version2)

api_v2.add_resource(Products, '/products')
api_v2.add_resource(Single_Product, '/products/<product_id>')
api_v2.add_resource(Update_Product, '/products/<product_id>')
api_v2.add_resource(Login, '/login')
api_v2.add_resource(SignUp, '/signup')
