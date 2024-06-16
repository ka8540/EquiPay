from flask import jsonify, make_response
from flask_restful import Resource, reqparse

try:
    from src.db.signup import user_signup, list_info_items
except ImportError:
    from db.signup import user_signup, list_info_items

class SignUpApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

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

        user_data = {
            'username': args['username'],
            'password': args['password'],
            'email': args['email'],
            'firstname': args['firstname'],
            'lastname': args['lastname']
        }
        
        response, status_code = user_signup(self.bcrypt, **user_data)
        return make_response(jsonify(response), status_code)
