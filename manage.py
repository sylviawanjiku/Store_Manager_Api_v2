 #  define an entry point to start our app
from app.apps import create_app
from flask_script import Manager
import os
from app.api.v2.models_v2.models import User,Product,Sales

app = create_app(os.getenv('FLASK_ENV'))

manager = Manager(app)
@manager.command
def migrate():
    """ create tables """
    User().create()
    Product().create()
    Sales().create()

@app.cli.command()
def drop():
    """ drop tables if they exist """
    User().drop()
    Product().drop()
    Sales().drop()

# add admin to db
@manager.command
def create_admin():
    """ add admin """
    user = User(username='SylviaW', first_name = 'Sylvia',last_name = 'Mbugua',password ='Admin!23', email='sylviawanjiku@gmail.com',
                is_admin=True)
    user.add()


if __name__=='__main__':
    manager.run()