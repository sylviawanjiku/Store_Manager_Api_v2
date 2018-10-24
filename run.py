#  define an entry point to start our app
from app.apps import create_app
import os

app = create_app(os.getenv('FLASK_ENV'))


if __name__=='__main__':
    app.run(debug=True)