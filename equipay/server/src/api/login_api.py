from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit
from model.user import generate_session_key
from db.login import check_user_credentials  # Importing the function from login.py

bcrypt = Bcrypt()

class LoginAPI(Resource):
    def __init__(self, **kwargs):
        self.bcrypt = kwargs['bcrypt']

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        args = parser.parse_args()

        # Use the check_user_credentials function from login.py
        response, status_code = check_user_credentials(self.bcrypt, args['username'], args['password'])
        
        if status_code == 200:
            access_token = create_access_token(identity={"username": args['username'], "session_key": response['sessionKey']})
            return make_response(jsonify(access_token=access_token, sessionKey=response['sessionKey']), 200)
        else:
            return make_response(jsonify(response), status_code)
