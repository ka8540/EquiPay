from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id
from db.delete_group import add_member_in_group, check_total_members, check_member 

class AddGroupMembersAPI(Resource):
    @jwt_required()
    def put(self,group_id):
        current_user_username = get_jwt_identity()['username']
        print("User credentials:", current_user_username)

        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', type=int, required=True, help="Friend ID cannot be blank!")
        args = parser.parse_args()

        friend_id = args['friend_id']
        
        total_members = check_total_members(group_id)
        if not total_members:
            return make_response(jsonify({"message":"Total Members Limit Exceeded!!"}),201)
        
        member = check_member(group_id,friend_id)
        if not member:
            return make_response(jsonify({"message":"Member Already exist"}),202)

        add_member = add_member_in_group(group_id,friend_id)

        if not add_member:
            return make_response(jsonify({"error":"Error Adding the User"}),401)
        
        return make_response(jsonify({"Success":"Added User Successfully"}),200)

        

        
