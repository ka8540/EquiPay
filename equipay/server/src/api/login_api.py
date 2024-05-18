"""
API Endpoints for user management and authentication.

These endpoints handle user registration and login functionality.
"""
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse
import hashlib  # Used for password hashing

# Try to import the necessary functions and classes explicitly
try:
    from src.utilities.swen_344_db_utils import exec_get_all  # Assuming this function is used within check_user_credentials
    from src.db.login import check_user_credentials # Ensure this is the correct function used for login logic
except ImportError:
    from utilities.swen_344_db_utils import exec_get_all
    from db.login import check_user_credentials


class LoginAPI(Resource):
    """
    API endpoint for user login.
    """

    def post(self):
        """
        Handles POST requests for user login.

        Expects JSON payload with the following parameters:
        - username (str): Username of the user.
        - password (str): Password of the user.

        Returns:
            JSON response with user ID if login is successful, otherwise returns an error message.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        args = parser.parse_args()

        # Hash the password using SHA-224 algorithm
        hashed_password = hashlib.sha224(args['password'].encode()).hexdigest()

        # Check user credentials
        print("reached here")
        response, status_code = check_user_credentials(args['username'], hashed_password)
        
        print("username:"+args['username']+"password:"+args['password']+"hashed_password:"+hashed_password)
        
        if response:
            # If credentials are correct, return JSON response with user ID
            return make_response(jsonify(response),status_code)
        else:
            response = "Cannot Login"
            # If credentials are incorrect, return an error message
            return make_response(jsonify(response),status_code)
