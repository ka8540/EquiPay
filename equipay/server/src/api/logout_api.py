"""
API Endpoints for user management and authentication.

These endpoints handle user registration and login functionality.
"""
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse

# Import only the necessary functions from utilities and logout db module
try:
    from src.utilities.swen_344_db_utils import exec_commit
    from src.db.logout import user_logout  # Assuming user_logout function handles the logout process
except ImportError:
    from utilities.swen_344_db_utils import exec_commit
    from db.logout import user_logout


class LogoutAPI(Resource):
    """
    API endpoint for user logout.
    """

    def post(self):
        print("idhar aa gaya")
        print("Raw Request Data:", request.data)
        parser = reqparse.RequestParser()
        print(parser)
        parser.add_argument('session_key', type=str, required=True, location='json')
        args = parser.parse_args()
        print(args,'session_key on api')

        # Check user credentials
        response, status_code = user_logout(args)

        return make_response(jsonify(response),status_code)
    
        

