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

class User(Data_base):

    def __init__(self,username=None,first_name=None,last_name = None,password = None,email = None ,is_admin = False):
        super().__init__()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        if password:    
            self.hash_password = generate_password_hash(password)
        self.email = email
        self.is_admin = is_admin

    def create(self):
        """create a table for the users"""
        self.create_table(
           """
            CREATE TABLE users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                password VARCHAR NOT NULL,
                email  VARCHAR NOT NULL,                
                is_admin BOOLEAN NOT NULL
            );
        )""")

    def drop(self):
        """Drop the table for users if it exists""" 
        self.drop_table('users')

    def add(self):
        """Add a user to the created table users"""
        insert_user = "INSERT INTO users(username,first_name,last_name,password,email,is_admin) VALUES( %s, %s, %s, %s, %s, %s)"
        user_data = (self.username, self.first_name, self.last_name ,self.hash_password ,self.email,self.is_admin)
        self.cur.execute(insert_user,user_data)
        self.save()

    def mapped_user(self, user_data):
        """Map a user to an object"""

        self.id = user_data[0]
        self.username =  user_data[1]
        self.first_name =  user_data[2]
        self.last_name =  user_data[3]
        self.hash_password = user_data[4]
        self.email =  user_data[5]
        self.is_admin =  user_data[6]

        return self

    def fetch_by_email(self,email):
        "Fetch a user through email"
        self.cur.execute("SELECT * FROM users WHERE email =%s", (email,))
        selected_user = self.cur.fetchone()
        if selected_user:
            return self.mapped_user(selected_user)
        return None

    def fetch_by_username(self,username):
        "Fetch a user through username"
        self.cur.execute("SELECT * FROM users WHERE username =%s", (username,))
        selected_user = self.cur.fetchone()
        if selected_user:
            return self.mapped_user(selected_user)
        return None

    def serialize(self):
        """put the user_data into a dictionary form"""
        return dict(
        id =self.id,
        username = self.username,
        first_name = self.first_name,
        last_name = self.last_name,
        hash_password = self.hash_password,
        email = self.email,
        is_admin = self.is_admin
        )


class Product(Data_base):
    def __init__(self,product_id=None, product_name=None, brand=None, quantity=None, price=None,avail_stock=None ,min_stock=None, uom=None, category=None):
        self.product_id = product_id
        self.product_name = product_name
        self.brand = brand
        self.quantity =quantity
        self.price = price
        self.avail_stock = avail_stock
        self.min_stock = min_stock
        self.uom = uom
        self.category = category

    def create(self):
        """ create table products """
        self.create_table(
            """
            CREATE TABLE products (
                id serial PRIMARY KEY,
                product_id VARCHAR NOT NULL,
                product_name VARCHAR NOT NULL,
                brand VARCHAR NOT NULL,
                quantity INTEGER,
                price INTEGER,
                avail_stock INTEGER, 
                min_stock INTEGER,
                uom VARCHAR,                
                category VARCHAR,
            );
            """
        )
    
    def drop(self):
        """ drop table products if it already exists """
        self.drop_table('products')

    
    def add(self):
        """Add a product to the created table products """
        insert_product="INSERT INTO products(product_id, product_name, brand, quantity, price,avail_stock ,min_stock, uom, category) VALUES (%s, %s, %s,%d,%d,%d,%d,%s,%s )"
        product_data = ( self.product_id,self.product_name,self.brand,self.quantity,self.price,self.avail_stock,self.min_stock,self.uom,self.category)
        self.cur.execute(insert_product,product_data)
        self.save()

    def mapped_product(self,product_data):
        """map the product details to an object"""
        self.id = product_data[0]
        self.product_id =  product_data[1]
        self.product_name =  product_data[2]
        self.brand =  product_data[3]
        self.quantity =  product_data[4]
        self.price =  product_data[5]
        self.avail_stock =  product_data[6]
        self.min_stock =  product_data[7]
        self.uom =  product_data[8]
        self.category = product_data[9]
        
        return self
    
    def fetch_by_id(self,product_id):
        """fetch a single product by id"""
        self.cur.execute("SELECT * FROM products WHERE id =%s",(product_id,))
        selected_product = self.cur.fetchone()
        if selected_product:
            return self.mapped_product(selected_product)
        return None

    def update(self,product_id):
        """update an existing product details"""

        self.cur.execute(
            """ UPDATE product SET product_id =%s,product_name =%s, brand= %s,quantity= %d,price = %d, avail_stock = %d, min_stock = %d, uom = %s,category= %s WHERE id =%s""",(
            self.product_id,self.product_name,self.brand,self.quantity,self.price,self.avail_stock,self.min_stock,self.uom,self.category)
        )
        self.save()
        self.close()
               
       
    def serialize(self):
        """put the procuct data in form of a dictionary"""
        return dict(
            id= self.id,
            product_id =  self.product_id,
            product_name =  self.product_name,
            brand =  self.brand,
            quantity =  self.quantity,
            price =  self.price,
            avail_stock =  self.avail_stock,
            min_stock =  self.min_stock,
            category = self.category
        )


    