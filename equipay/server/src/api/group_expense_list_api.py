from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id
from db.group import get_group_expenses

class GroupExpensesListAPI(Resource):
    @jwt_required()
    def get(self, group_id):
        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)

        expenses = get_group_expenses(user_id, group_id)
        formatted_expenses = [
            {
                "expense_id": expense[0],
                "description": expense[1],
                "total_amount": "{:.2f}".format(float(expense[2])),
                "payer_name": expense[3],
                "date": expense[4],
                "status": "lend" if float(expense[5]) > 0 else "borrowed",
                "amount": "{:.2f}".format(abs(float(expense[5])))
            } for expense in expenses
        ]
        return jsonify(formatted_expenses)
