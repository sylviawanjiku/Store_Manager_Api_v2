from datetime import datetime

from werkzeug.security import generate_password_hash,check_password_hash

import psycopg2

# local imports
from flask import current_app

class Data_base:
    """"database connection model"""

    def __init__(self):
        self.db_host = current_app.config['DB_HOST']
        self.db_username = current_app.config['DB_USERNAME']
        self.db_password = current_app.config['DB_PASSWORD']
        self.db_name = current_app.config['DB_NAME']

        # connect to the storemanager database
        self.connect = psycopg2.connect(
            host=self.db_host,
            user=self.db_username,
            password =self.db_password,
            database =self.db_name
        )
        # open cursor for performing database operations
        self.cur =self.connect.cursor()

    def create_table(self,schema):
        """method for creating tables"""
        self.cur.execute(schema)
        self.save()

    def drop_table(self,name):
        """method for dropping tables"""
        self.cur.execute("DROP TABLE IF EXISTS " + name)
        self.save()

    def save(self):
        """method for saving a change made"""
        self.connect.commit()

    def close(self):
        """method for closing the cursor"""
        self.cur.close()




    
