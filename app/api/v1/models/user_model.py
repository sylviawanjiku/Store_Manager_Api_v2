"""
This module defines the user model and associated functions
"""
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256 as sha256
import datetime


users = []

class UserModel():

    @staticmethod
    def create_user(username,first_name,last_name,password,email):      
        user_data = dict(
            id =  len(users),
            username = username,
            first_name= first_name,
            last_name = last_name,
            password = password,
            email = email
                       
        )
        users.append(user_data)
        return users


    @staticmethod
    def get_all_users():
        # fetch all users
        return  users

# checks if user  with the email exists
    @staticmethod
    def find_by_email(email):
        # fetch all users
        return next((item for item in users if item["email"] == email), False)

# hash user password
    @staticmethod
    def hash_password(raw_password):
         
        return  sha256.hash(raw_password)


# verify if password provided by user matches the hashed password stored in users
    @staticmethod
    def verify_password(password,email):
        for x in users:
            listOfKeys =[key for (key,value) in x.items() if value == email]
            if listOfKeys :
                result = list(filter(lambda person:person['email'] == email,users))
                return sha256.verify(password, result[0]['password'])
        


    
