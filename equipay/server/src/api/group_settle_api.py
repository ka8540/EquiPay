from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import boto3
from botocore.exceptions import NoCredentialsError
import werkzeug
from db.amoutowed import get_user_id
from db.group import delete_group_debt

    
class DeleteGroupDebtByIdAPI(Resource):
    @jwt_required()
    def post(self,group_id):
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', type=int, required=True, help="Friend ID cannot be blank!")
        parser.add_argument('amount_owed', type=float, required=True, help="Amount owed cannot be blank!")
        args = parser.parse_args()  

        # Get user ID from JWT token
        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)

        if not user_id:
            return make_response(jsonify({"error": "User not found"}), 404)

        # Attempt to delete the debt
        success = delete_group_debt(user_id, args['friend_id'], args['amount_owed'],group_id)
        
        if success:
            return make_response(jsonify({"message": "Debt record deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Failed to delete debt record"}), 400)
    