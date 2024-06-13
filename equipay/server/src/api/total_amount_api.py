from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import calculate_amount_owed, get_user_id , get_user_debts
from utilities.swen_344_db_utils import exec_get_one 


class TotalAmountAPIbyID(Resource):
    @jwt_required()
    def get(self, friend_id):
        current_user_id = get_jwt_identity()['username']
        print("User credentials:", current_user_id)
        UserID_query = '''SELECT user_id FROM "user" WHERE username = %s;'''
        user_id_results = exec_get_one(UserID_query, (current_user_id,))
        print("User_ID:", user_id_results)
        if not user_id_results:
            print("No user found with username:", current_user_id)
            return jsonify({"message": "User not found"}), 404
        user_id = user_id_results[0]
        print("user_id:", user_id)
        print(f"Calculating total amount for user ID {user_id} with friend ID {friend_id}")

        # Calculate total amount owed by the user to the friend
        amount_owed_by_user = calculate_amount_owed(user_id, friend_id)

        # Calculate total amount owed by the friend to the user
        amount_owed_to_user = calculate_amount_owed(friend_id, user_id)

        # Calculate the net amount
        net_amount = amount_owed_to_user - amount_owed_by_user

        if net_amount < 0:
            message = f"You owe {abs(net_amount)}"
        else:
            message = f"You are owed {net_amount}"

        return jsonify({"message": message, "net_amount": net_amount})


class TotalAmountAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_username = get_jwt_identity()['username']
        print("User credentials:", current_user_username)

        user_id = get_user_id(current_user_username)
        if not user_id:
            return jsonify({"message": "User not found"}), 404

        debts = get_user_debts(user_id)
        results = [] 
        for friend_id, friend_name, net_amount in debts:
            if net_amount != 0: 
                results.append({
                    "friend_id": friend_id,  
                    "friend_name": friend_name,
                    "net_amount": float(net_amount) 
                })

        print("Debt results:", results)
        return jsonify(results)

