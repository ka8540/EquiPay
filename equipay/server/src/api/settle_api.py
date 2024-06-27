from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import boto3
from botocore.exceptions import NoCredentialsError
import werkzeug
from db.amoutowed import get_user_id
from db.amoutowed import get_debts_by_friend, delete_debt
from utilities.swen_344_db_utils import exec_commit
from db.activity import get_firstname_by_id
class DebtsByFriendAPI(Resource):
    @jwt_required()
    def get(self, friend_id):
        jwt_user = get_jwt_identity()
        user_id = get_user_id(jwt_user['username'])

        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)

        debts = get_debts_by_friend(user_id, friend_id)
        if not debts:
            return make_response(jsonify({"message": "No debts found"}), 201)

        return jsonify(debts)
    
class DeleteDebtAPI(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', type=int, required=True, help="Friend ID cannot be blank!")
        args = parser.parse_args()  

        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        firstname = get_firstname_by_id(user_id)
        if not user_id:
            return make_response(jsonify({"error": "User not found"}), 404)

        friend_user_id = args['friend_id']

        friend_name = get_firstname_by_id(friend_user_id)

        success = delete_debt(user_id, friend_user_id)
        if success:
            log_details = f"{firstname} has settled up with {friend_name}."
            log_sql = "INSERT INTO ActivityLog (UserID, ActionType, Details) VALUES (%s, %s, %s)"
            exec_commit(log_sql, (user_id, 'Settled Debt', log_details))

            return make_response(jsonify({"message": "Debt record deleted successfully"}), 200)
        else:
            return make_response(jsonify({"message": "No Debt Record"}), 201)
    