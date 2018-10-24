from flask import Flask, make_response, jsonify, request
from ..models.user_model import UserModel
from flask_restful import Resource, reqparse
from datetime import date, datetime, timedelta
from passlib.hash import sha256_crypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity,get_raw_jwt)
from instance.config import secret_key
import re

parser =reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('email')
parser.add_argument('first_name') 
parser.add_argument('last_name') 
parser.add_argument('email')
parser.add_argument('password')


""" Create a function that generates authentication"""

class User(Resource): 
    def post(self):
            '''Posting items to Users'''        
            args = parser.parse_args()
            username = args.get('username')
            first_name= args.get('first_name')
            last_name = args.get('last_name')
            email = args.get('email')
            raw_password = args.get('password')  

# validate user input
            if not username:
                 return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'username cannot be null'                   
                }
            ), 400)
            if not first_name:
                  return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'first_name cannot be null',
                    
                }
            ), 400)
            if not last_name:
                  return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'last_name cannot be null',
                    
                }
            ), 400)
            if not email:
                  return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'email cannot be null',
                    
                }
            ), 400)
            if not raw_password:
                  return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'password cannot be null',
                    
                }
            ), 400)

            # validate user input
            email_format = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)")

            if not (re.match(email_format, email)):
                return make_response(jsonify({'message' : 'Invalid email'}), 400)

            if len(raw_password) < 8:
                return make_response(jsonify({'message' : 'Password should be atleast 8 characters'}), 400)
            
            #  check if email already exist 
            this_user = UserModel.find_by_email(email)
            if this_user != False:
                return {'message': 'email already exist'},400 
               
               
            # generate hash password
            password = UserModel.hash_password(raw_password)
            user = UserModel.create_user(username,first_name,last_name,password,email)
            all_users = UserModel.get_all_users()
            return make_response(jsonify(
                {
                    'status': 'Ok',
                    'Message': 'User created successfully',
                    'product': all_users
                }
            ), 201)
            # return {"message":"",all_users}, 
           

class Login(Resource):    
    parser =reqparse.RequestParser()
    parser.add_argument('email')
    parser.add_argument('password')
    def post(self):
            args = parser.parse_args()
            email = args.get('email')
            password = args.get('password')

            if not email:
                return {"message":"email cannot be null"}

            if not password:
                return {"message":"password cannot be null"}


# after validation check if user exists by email            
            current_user = UserModel.find_by_email(email)
            if current_user == 0:
                  return {"message":"user with the email doesnt exist"}


# check if user password and stored hashed password match
            password_match = UserModel.verify_password(password,email)
            if password_match == True:
                access_token = create_access_token(identity = email)

                return {
                         "message":"logged in successfully",
                         "access_token":access_token
                         }        

            return {"message":"wrong credentials"}
  