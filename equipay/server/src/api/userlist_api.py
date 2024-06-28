from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

try:
    from src.db.user_details import list_info_items
    from src.model.user import check_session_key, get_username
except ImportError:
    from db.user_details import list_info_items
    from model.user import check_session_key, get_username

class ListUsersApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

    @jwt_required()
    def get(self):
        session_key = request.headers.get('session_key') or request.headers.get('Session-Key')
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)
        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"message": "Invalid session key"}), 401)
        current_user = get_jwt_identity()

        return jsonify(list_info_items(username))

