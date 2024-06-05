from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt

try:
    from src.utilities.swen_344_db_utils import exec_commit
    from src.model.user import check_session_key, get_username
    from db.user_details import get_password , update_passord , delete_account
except ImportError:
    from utilities.swen_344_db_utils import exec_commit
    from model.user import check_session_key, get_username
    from db.user_details import get_password , update_passord, delete_account

class DeleteAccountApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

    @jwt_required()
    def post(self):
        print("Reached DeleteAccount POST endpoint")
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

        result = delete_account(username)

        if not result:
            return make_response(jsonify({"message": "Failed to Delete Account"}), 404)
        
        return make_response(jsonify({"message":"Account is Deleted Successfully "}),200)

        
