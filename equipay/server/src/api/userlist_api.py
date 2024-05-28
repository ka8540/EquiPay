from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

try:
    from src.db.signup import list_info_items
    from src.model.user import check_session_key
except ImportError:
    from db.signup import list_info_items
    from model.user import check_session_key

class ListUsersApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

    @jwt_required()
    def get(self):
        print("Reached ListUsersApi GET endpoint")
        
        # Log all incoming headers for debugging
        print("Headers received:", request.headers)

        # Adjust to handle different variations of session_key header
        session_key = request.headers.get('session_key') or request.headers.get('Session-Key')
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)

        print("Session Key:", session_key)

        # Verify session key
        if not check_session_key(session_key):
            return make_response(jsonify({"message": "Invalid session key"}), 401)

        # Get user identity from JWT
        current_user = get_jwt_identity()

        # If session key is valid, return the list of users
        return jsonify(list_info_items())
