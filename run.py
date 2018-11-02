"""define an entry point to start our app"""
from app.apps import create_app
import os

app = create_app(os.getenv('FLASK_ENV'))

if __ name _ == '__main__':
    app.run(debug=True)
