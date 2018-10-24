from flask import Flask
from flask_restful import Api
from .api.v1 import version1 as v1
from flask_jwt_extended import JWTManager


from instance.config import app_config



# The create_app function wraps the creation of a new Flask object, and returns it after it's loaded up with configuration settings
def create_app(config_name):
    app =Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False



    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(v1)

# jwt initialization
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)
    


    return app
