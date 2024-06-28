from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import werkzeug
from db.group import get_group_members_by_group_id , get_groups_by_group_id
from db.amoutowed import get_user_id


class GroupMembersAPI(Resource):
    @jwt_required()
    def get(self, group_id):
        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        try:
            members = get_group_members_by_group_id(group_id)
            if not members:
                return make_response(jsonify({"message": "No members found in the group"}), 404)
            return jsonify(members)
        except Exception as e:
            print(f"Error fetching group members: {str(e)}")
            return make_response(jsonify({"error": "An error occurred while fetching group members", "details": str(e)}), 500)
        

class GroupNameByIdAPI(Resource):
    @jwt_required()  
    def get(self, group_id):
        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        try:
            group_name = get_groups_by_group_id(group_id)
            if not group_name:
                return make_response(jsonify({"message": "No group name found"}), 404)
            return jsonify({"group_name": group_name[0][0]}) if group_name else make_response(jsonify({"message": "Group not found"}), 404)
        except Exception as e:
            print(f"Error fetching group name: {str(e)}")
            return make_response(jsonify({"error": "An error occurred while fetching the group name", "details": str(e)}), 500)
