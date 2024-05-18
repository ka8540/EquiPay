from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse


# Import only the necessary functions from the signup module
try:
    from src.db.signup import user_signup, list_info_items
except ImportError:
    from db.signup import user_signup, list_info_items


class SignUpApi(Resource):
    def get(self):
        return jsonify(list_info_items())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('firstname', type=str, required=True, location='json')
        parser.add_argument('lastname', type=str, required=True, location='json')
        args = parser.parse_args()
        
        print(args["username"]+args["password"]+args["email"]+args["firstname"]+args["lastname"])

        response, status_code = user_signup(**args)
        return make_response(jsonify(response), status_code)
