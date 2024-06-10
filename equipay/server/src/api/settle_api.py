from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import boto3
from botocore.exceptions import NoCredentialsError
import werkzeug
from db.amoutowed import get_user_id
from db.amoutowed import get_debts_by_friend, delete_debt

class DebtsByFriendAPI(Resource):
    @jwt_required()
    def get(self, friend_id):
        jwt_user = get_jwt_identity()
        user_id = get_user_id(jwt_user['username'])

        if not user_id:
            return jsonify({"message": "User not found"}), 404

        debts = get_debts_by_friend(user_id, friend_id)
        if not debts:
            return jsonify({"message": "No debts found"}), 404

        return jsonify(debts)
    
class DeleteDebtAPI(Resource):
    @jwt_required()
    def post(self):
        # Parse the input data
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
        success = delete_debt(user_id, args['friend_id'], args['amount_owed'])
        
        if success:
            return make_response(jsonify({"message": "Debt record deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Failed to delete debt record"}), 400)
    