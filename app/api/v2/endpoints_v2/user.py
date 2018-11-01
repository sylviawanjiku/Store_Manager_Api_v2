from flask_restful import Resource, reqparse
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token,get_jwt_identity)
from .authentication import admin_only
# local imports
from ...v2.models_v2.models import User
from utils import validator

# request data validation
parser =reqparse.RequestParser()
parser.add_argument('username',type=str, required=True, help="Username cannot blank")
parser.add_argument('email',type=str, required=True, help="Email cannot be blank")
parser.add_argument('first_name',type=str, required=True, help="First Name cannot be bank")
parser.add_argument('last_name',type=str, required=True, help="Last Name cannot be blank")
parser.add_argument('password', required=True, help="Password cannot be blank")
parser.add_argument('is_admin', required=True, help="Is_admin cannot be blank")


class SignUp(Resource):
        @jwt_required
        @admin_only 
        def post(self):  
            args = parser.parse_args()
            username = args.get('username')
            first_name= args.get('first_name')
            last_name = args.get('last_name')
            password = args.get('password')
            email = args.get('email')
            is_admin = args.get('is_admin')
          

            validate = validator.Validators()

            if not validate.validate_email(email):
                return {"message": "enter valid email"}, 400

            if not validate.validate_username(username):
                return {"message": "username must be a string"}, 400
            
            if not validate.validate_username(first_name):
                return {"message": "Firstname must be a string"}, 400

            if not validate.validate_username(last_name):
                return {"message": "Lastname must be a string"}, 400

            if not validate.validate_password(password):
                return{"message":"Password should start with a capital letter and include a number"}

            if User().fetch_by_email(email):
                return{"message":"User already exists"},400

            if User().fetch_by_username(username):
                return{"message":"User already exists"},400

            user =User(username,first_name, last_name, password,email,is_admin)       
            user.add()

            return{"message":"user created successfully"},201

# class Make_Admin(Resource):
#     @jwt_required
#     @admin_only
#     def put(self, user_id):
#         """Update a single user details"""
#         args = parser.parse_args()
#         is_admin = args['is_admin']
#         user = User(is_admin)
#         user = User().fetch_user_by_id(user_id)
#         return user
#             # user = User(is_admin)
#         #     print(user)
#         #     user.update(user_id)
#         #     return{"message":"User updated successfully updated"},200
#         # return{"message":"User not found"},404
        
          
