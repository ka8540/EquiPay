from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt

try:
    from src.utilities.swen_344_db_utils import exec_commit
    from src.model.user import check_session_key, get_username
    from db.user_details import get_password , update_passord
except ImportError:
    from utilities.swen_344_db_utils import exec_commit
    from model.user import check_session_key, get_username
    from db.user_details import get_password , update_passord

class PasswordApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('old_password', type=str, required=True, help="Old password is required")
        self.req_parser.add_argument('new_password', type=str, required=True, help="New password is required")

    @jwt_required()
    def post(self):
        args = self.req_parser.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']
        session_key = request.headers.get('session_key') or request.headers.get('Session-Key')
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)
        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"message": "Invalid session key"}), 401)
        stored_password = get_password(username,old_password)
        if not stored_password:
            return make_response(jsonify({"message": "Password is Incorrect"}), 404)
        new_password_hash = self.bcrypt.generate_password_hash(new_password).decode('utf-8')
        result = update_passord(new_password_hash, username)
        return make_response(jsonify({"message": "Password Updated Sucessfully"}), 200)
