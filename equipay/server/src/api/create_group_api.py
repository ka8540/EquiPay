from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import werkzeug
from db.group import get_groups_by_user_id, create_group, add_group_member
from db.amoutowed import get_user_id

class UserGroupsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_username = get_jwt_identity()['username']

        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)

        try:
            groups = get_groups_by_user_id(user_id)
            if not groups:
                return make_response(jsonify({"message": "No groups found"}), 201)
            return jsonify(groups)
        except Exception as e:
            print(f"Error fetching groups: {str(e)}")
            return make_response(jsonify({"error": "An error occurred while fetching groups", "details": str(e)}), 500)
    
class CreateGroupAPI(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('friend_ids', type=int, action='append', help="List of friend IDs can be empty.")
        parser.add_argument('profile_picture_url', type=str, required=True, help="Profile picture URL cannot be blank!")
        parser.add_argument('group_name', type=str, required=True, help="Group name cannot be blank!")
        args = parser.parse_args()

        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"error": "User not found"}), 404)

        group_id = create_group(args['group_name'], user_id, args['profile_picture_url'])
        if group_id is None:
            return make_response(jsonify({"error": "Failed to create group"}), 400)

        add_group_member(group_id, user_id, True)

        if args['friend_ids']:
            for friend_id in args['friend_ids']:
                add_group_member(group_id, friend_id, False)

        return make_response(jsonify({"message": "Group created successfully", "group_id": group_id}), 200)
    


