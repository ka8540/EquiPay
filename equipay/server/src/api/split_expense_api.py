from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.split_expense import split_expense_

class SplitExpenseTwoApi(Resource):
    @jwt_required()
    def post(self):
        print("Inside the POST request of Split Two")
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, required=True, help="Amount cannot be blank!")
        parser.add_argument('friend_ids', type=int, action='append', required=True, help="Friend IDs list cannot be blank!")
        parser.add_argument('include_self', type=bool, required=True, help="Include self in split cannot be blank!")
        parser.add_argument('description', type=str, required=True, help="Description cannot be blank!!")
        args = parser.parse_args()
        
        print(args['amount'])
        print(args['friend_ids']) 
        print(args['include_self'])
        
        current_user_id = get_jwt_identity()['username']
        result = split_expense_(current_user_id, args['amount'], args['friend_ids'], args['include_self'], args['description'])
        if result:
            return make_response(jsonify({"message": "Expense split successfully."}), 200)
        else:
            return make_response(jsonify({"message": "Failed to split expense."}), 500)
