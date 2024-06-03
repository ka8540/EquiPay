from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

try:
    from src.db.user_details import update_user_detail,list_user_detail
    from src.model.user import check_session_key, get_username
except ImportError:
    from db.user_details import update_user_detail,list_user_detail
    from model.user import check_session_key, get_username

class AccountApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('email', type=str, required=False, help='Email to update')
        self.req_parser.add_argument('firstname', type=str, required=False, help='First name to update')
        self.req_parser.add_argument('lastname', type=str, required=False, help='Last name to update')
        self.req_parser.add_argument('username', type=str, required=False, help='Username to update')

    @jwt_required()
    def get(self):
        print("Reached Account_API GET endpoint")
        
        # Log all incoming headers for debugging
        print("Headers received:", request.headers)

        # Adjust to handle different variations of session_key header
        session_key = request.headers.get('session_key') or request.headers.get('Session-Key')
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)

        print("Session Key:", session_key)

        # Verify session key
        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"message": "Invalid session key"}), 401)
        
        print("Username associated with session key:", username)

        # Get user identity from JWT
        current_user = get_jwt_identity()

        # If session key is valid, return the list of users excluding the current user
        return jsonify(list_user_detail(username))

    @jwt_required()
    def put(self):
        print("Reached Account_API PUT endpoint")
        
        # Log all incoming headers for debugging
        print("Headers received:", request.headers)
        
        # Adjust to handle different variations of session_key header
        session_key = request.headers.get('session_key') or request.headers.get('Session-Key')
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)

        print("Session Key:", session_key)

        # Verify session key
        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"message": "Invalid session key"}), 401)
        
        print("Username associated with session key:", username)

        # Get user identity from JWT
        current_user = get_jwt_identity()

        args = self.req_parser.parse_args()
        
        # Filter out None values from args, if any field wasn't provided in the request
        update_args = {key: value for key, value in args.items() if value is not None}
        
        # Update user details in the database
        update_result = update_user_detail(username, **update_args)

        if update_result:
            return jsonify({"message": "User details updated successfully"})
        else:
            return make_response(jsonify({"message": "Failed to update user details"}), 500)

