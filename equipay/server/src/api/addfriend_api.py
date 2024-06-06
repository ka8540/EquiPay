from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from db.friends import existing_friend, add_friend_request , get_pending_friend_requests , update_friend_request_status , get_friend_requests

class AddFriendApi(Resource):
    @jwt_required()
    def get(self):
        print("Entered the GET Request of Add Friend ")
        current_user_id = get_jwt_identity()
        username = current_user_id['username']  
        print("username:",username)
        try:
            friend_requests = get_pending_friend_requests(username)
            print(friend_requests)
            return make_response(jsonify(friend_requests), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)

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
        
    @jwt_required()
    def put(self):
        print("Inside the PUT request!!")
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', required=True, help="Friend ID cannot be blank!")
        parser.add_argument('action', required=True, help="Action must be specified (accept or reject)!")
        args = parser.parse_args()
        action = args['action']
        print("Action:",action)
        friend_id = int(args['friend_id'])
        print("friend_id:",friend_id)
        current_user_id = get_jwt_identity()
        username = current_user_id['username']
        if update_friend_request_status(username, friend_id, action):
            return make_response(jsonify({"message": "Friend request updated successfully"}), 200)
        else:
            return make_response(jsonify({"message": "Failed to update friend request"}), 500)       


class FiendList(Resource):
    @jwt_required()
    def get(self):
        print("Entered the GET Request of Add Friend ")
        current_user_id = get_jwt_identity()
        username = current_user_id['username']  
        print("username:",username)
        try:
            friend_requests = get_friend_requests(username)
            print(friend_requests)
            return make_response(jsonify(friend_requests), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
