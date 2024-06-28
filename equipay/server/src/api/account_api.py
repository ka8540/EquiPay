from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from db.amoutowed import get_user_id
from db.activity import get_firstname_by_id
try:
    from src.db.user_details import update_user_detail, list_user_detail
    from src.model.user import get_username
except ImportError:
    from db.user_details import update_user_detail, list_user_detail
    from model.user import get_username

bcrypt = Bcrypt()

class AccountApi(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('email', type=str, required=False)
        self.req_parser.add_argument('firstname', type=str, required=False)
        self.req_parser.add_argument('lastname', type=str, required=False)
        self.req_parser.add_argument('username', type=str, required=False)

    @jwt_required()
    def get(self):
        session_key = request.headers.get('session_key', None)
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)

        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"message": "Invalid session key"}), 401)

        return jsonify(list_user_detail(username))

    @jwt_required()
    def put(self):
        session_key = request.headers.get('session_key', None)
        if not session_key:
            return make_response(jsonify({"message": "Missing session key"}), 400)

        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"message": "Invalid session key"}), 401)

        args = self.req_parser.parse_args()
        args.pop('username', None)
        update_result = update_user_detail(username, **args)
        if update_result:
            return jsonify({"message": "User details updated successfully"})
        else:
            return make_response(jsonify({"message": "Failed to update user details"}), 500)


class FriendNameAPI(Resource):
    @jwt_required()
    def get(self, friend_id):
        jwt_user = get_jwt_identity()
        user_id = get_user_id(jwt_user['username'])

        if not user_id:
            return make_response(jsonify({"error": "User not found"}), 404)

        friend_name = get_firstname_by_id(friend_id)  
        if not friend_name:
            return make_response(jsonify({"error": "No Name Found"}), 404)

        return jsonify({"friend_name": friend_name})
        

        


