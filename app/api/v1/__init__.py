from flask_restful import Api
from flask import Blueprint
from .endpoints.sales import SalesRecord
from .endpoints.products import Products
from .endpoints.user import User
from .endpoints.user import Login
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
# from .endpoints.user import SecretResource


version1 = Blueprint ('api',__name__, url_prefix='/api/v1')

api = Api(version1)

api.add_resource(Products, '/products','/products/<product_id>')
api.add_resource(SalesRecord, '/sales','/sales/<sale_id>')
api.add_resource(User, '/users','/users/<user_id>')
api.add_resource(Login, '/login')
# api.add_resource(SecretResource, '/secret')
