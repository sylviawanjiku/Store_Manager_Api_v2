from flask import Flask
from flask_restful import Resource ,reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token,jwt_required ,get_jwt_identity ,get_raw_jwt
from ..models_v2.models import User
from utils import validator
import datetime
from functools import wraps

blacklist = set()
# request data validation
parser =reqparse.RequestParser()

parser.add_argument('email',type=str, required=True, help="This field can not be left bank")
parser.add_argument('password', required=True, help="This field can not be left bank")


""" Create a function that generates authentication"""
def admin_only(f):
    ''' Deny access if the user is not admin '''
    @wraps(f)
    def decorator_func(*args,**kwargs):
        user = User().fetch_by_username(get_jwt_identity()["username"])
        if user["is_admin"] == False:
            return {'message': 'unauthorized access, Invalid token'}, 401
        return f(*args, **kwargs)
    return decorator_func
    
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

            # if not check_password_hash(user.hash_password, password):
            #     return {'message': 'incorrect password'}, 401

            expiry_time = datetime.timedelta(minutes =25)
            token = create_access_token(
                identity = user,
                expires_delta=expiry_time
                )
            return{"token":token ,"message":"User successfully logged In"}
    
