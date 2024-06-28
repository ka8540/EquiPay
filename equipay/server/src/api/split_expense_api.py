from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.split_expense import split_expense_
from utilities.swen_344_db_utils import exec_commit
from db.amoutowed import get_user_id
from db.activity import get_firstname_by_id
class SplitExpenseTwoApi(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, required=True)
        parser.add_argument('friend_ids', type=int, action='append', required=True)
        parser.add_argument('include_self', type=bool, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()

        current_user_id = get_jwt_identity()['username']
        result = split_expense_(current_user_id, args['amount'], args['friend_ids'], args['include_self'], args['description'])

        if result:
            user_id = get_user_id(current_user_id)
            firstname = get_firstname_by_id(user_id)
            payer_log_details = f"{firstname} added an expense of ${args['amount']} for '{args['description']}'."
            exec_commit("INSERT INTO ActivityLog (UserID, ActionType, Details) VALUES (%s, %s, %s)", 
                        (user_id, 'Added Expense', payer_log_details))
            for friend_id in args['friend_ids']:
                owe_amount = args['amount'] / (len(args['friend_ids']) + (1 if args['include_self'] else 0))
                friend_firstname = get_firstname_by_id(friend_id)
                friend_log_details = f"{friend_firstname} owes {firstname} ${owe_amount:.2f} for '{args['description']}'."
                exec_commit("INSERT INTO ActivityLog (UserID, ActionType, Details) VALUES (%s, %s, %s)", 
                            (friend_id, 'Incurred Debt', friend_log_details))

            return make_response(jsonify({"message": "Expense added and logged successfully."}), 200)
        else:
            return make_response(jsonify({"message": "Failed to split expense."}), 500)

