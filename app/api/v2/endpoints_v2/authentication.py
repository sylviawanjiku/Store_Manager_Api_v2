from flask import Flask
from flask_restful import Resource ,reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from ..models_v2.models import User
from utils import validator
import datetime


# request data validation
parser =reqparse.RequestParser()
parser.add_argument('username',type=str, required=True, help="This field can not be left bank")
parser.add_argument('email',type=str, required=True, help="This field can not be left bank")
parser.add_argument('first_name',type=str, required=True, help="This field can not be left bank")
parser.add_argument('last_name',type=str, required=True, help="This field can not be left bank")
parser.add_argument('email',type=str, required=True, help="This field can not be left bank")
parser.add_argument('password',type=str, required=True, help="This field can not be left bank")


""" Create a function that generates authentication"""

class SignUp(Resource): 
        def post(self):  
            args = parser.parse_args()
            username = args.get('username')
            first_name= args.get('first_name')
            last_name = args.get('last_name')
            email = args.get('email')
            password = args.get('password')

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
                return{"message":"Password should include a number and start with a capital lettter"}

            if User().fetch_by_email(email):
                return{"message":"User already exists"},400

            if User().fetch_by_username(username):
                return{"message":"User already exists"},400

            user =User(username, email, first_name, last_name, password)       
            user.add()

            return{"message":"user created successfully"}

class Login(Resource):

    parser =reqparse.RequestParser()
    parser.add_argument('email')
    parser.add_argument('password')

    def post(self):
            args = parser.parse_args()
            email = args.get('email')
            password = args.get('password')

            user=User().fetch_by_email(email)

            if not user:
                return{"message":"User not found"},404

            if not check_password_hash(user.hash_password, password):
                return {'message': 'incorrect password'}, 401

            expiry_time = datetime.timedelta(minutes =25)
            token = create_access_token(
                identity = user.serialize(),
                expires_delta=expiry_time
                )
            return{"token":token ,"message":"User successfully logged In"}
       