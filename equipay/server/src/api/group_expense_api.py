from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.group import split_group_expense
from db.amoutowed import get_user_id

class GroupExpenseAPI(Resource):
    @jwt_required()
    def post(self, group_id):
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, required=True, help="Amount cannot be blank!")
        parser.add_argument('friend_ids', type=int, action='append', required=True, help="Friend IDs list cannot be blank!")
        parser.add_argument('include_self', type=bool, required=True, help="Include self in split cannot be blank!")
        parser.add_argument('description', type=str, required=True, help="Description cannot be blank!")
        args = parser.parse_args()

        print("Amount: ", args['amount'])
        print("Friend IDs: ", args['friend_ids'])
        print("Include Self: ", args['include_self'])
        print("Description: ", args['description'])
        
        # Obtain the current user's identity from JWT token
        current_user_username = get_jwt_identity()['username']
        
        # Pass the group_id from the URL to the expense splitting function
        result = split_group_expense(current_user_username, group_id, args['amount'], args['friend_ids'], args['include_self'], args['description'])
        if result:
            return make_response(jsonify({"message": "Expense split successfully."}), 200)
        else:
            return make_response(jsonify({"message": "Failed to split expense."}), 500)
