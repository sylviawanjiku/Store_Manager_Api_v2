import os
from app.apps import create_app
from app.api.v2.models_v2.models import Data_base, User, Product

app = create_app("testing")


def migrate():
    """Creating tables for testing"""
    User().create()
    Product().create()


def drop():
    """ drop tables if they exist """
    User().drop()
    Product().drop()


# add admin to db
def create_admin():
    """ add admin """
    user = User(username='SylviaW', first_name='Sylvia', last_name='Mbugua',
                password='Admin!23', email='sylviawanjiku@gmail.com',
                is_admin=True)
    user.add()
