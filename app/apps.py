from flask import Flask
from flask_restful import Api
from .api.v1 import version1 as v1
from .api.v2 import version2 as v2
from flask_jwt_extended import JWTManager
from .api.v2.endpoints_v2.authentication import blacklist
from .api.v2.endpoints_v2.v2_home import home
from instance.config import app_config


""" create_app function wraps the creation and return of Flaskobject """  
app = Flask(__name__, instance_relative_config=True)
app.url_map.strict_slashes = False    
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')
app.register_blueprint(v1)
app.register_blueprint(v2)
app.register_blueprint(home)

"""jwt initialization"""
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

return app
