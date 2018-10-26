#  define an entry point to start our app
from app.apps import create_app
import os
from app.api.v2.models_v2.models import User,Product

app = create_app(os.getenv('FLASK_ENV'))

@app.cli.command()
def migrate():
    """ create tables """
    User().create()
    Product().create()

@app.cli.command()
def drop():
    """ drop tables if they exist """
    User().drop()
    Product().drop()

# add admin to db
@app.cli.command()
def create_admin():
    """ add admin """
    user = User(username='Sylvia', first_name = 'Sylvia',last_name = 'Mbugua',password ='12345678', email='sylviawanjiku@gmail.com',
                is_admin=True)
    user.add()
    
if __name__=='__main__':
    app.run(debug=True)
