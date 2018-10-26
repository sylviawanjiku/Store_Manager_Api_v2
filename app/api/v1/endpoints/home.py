from flask import Flask, make_response, jsonify, request
from flask_restful import Resource
from flask_restful import Api
from flask import Blueprint

class Home(Resource):
    def get(self):
        return make_response(jsonify({
                    'message': 'Welcome to Store Manager'
                }))

home = Blueprint ('home',__name__)

api = Api(home)

api.add_resource(Home, '/')