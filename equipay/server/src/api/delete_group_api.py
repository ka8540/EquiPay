from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id
from db.delete_group import delete_group1
class DeleteGroupAPI(Resource):
    @jwt_required()
    def post(self,group_id):
        current_user_username = get_jwt_identity()['username']
        print("User credentials:", current_user_username)

        user_id = get_user_id(current_user_username)
        if not user_id:
            return jsonify({"message": "User not found"}), 404
        
        delete = delete_group1(user_id,group_id)
        if delete:
            return make_response(jsonify({"message:":"Group Delete Successfully"}),200)
        if not delete:
            return make_response(jsonify({"error:":"error deleting the group"}),201)
        
        

        