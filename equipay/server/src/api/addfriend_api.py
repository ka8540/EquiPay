from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from db.friends import existing_friend, add_friend_request

class AddFriendApi(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', required=True, help="Friend ID cannot be blank!")
        args = parser.parse_args()
        friend_id = int(args['friend_id'])
        current_user_id = get_jwt_identity()
        username = current_user_id['username'] 
        if existing_friend(username, friend_id):
            return make_response(jsonify({"message": "Friend request already exists"}), 409)
        if add_friend_request(username, friend_id):
            return make_response(jsonify({"message": "Friend request sent successfully"}), 200)
        else:
            return make_response(jsonify({"message": "Failed to send friend request"}), 500)
