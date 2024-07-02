from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id
from db.delete_group import leave_group

class LeaveGroupAPI(Resource):
    @jwt_required()
    def put(self,group_id):
        current_user_username = get_jwt_identity()['username']
        print("User credentials:", current_user_username)

        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        group = leave_group(user_id,group_id)
        if not group:
            return make_response(jsonify({"error:":"Error Leaving Group"}),404)
        return make_response(jsonify({"message":"Leaving group Successfully"}),200)
        
