from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.group import get_group_debts, calculate_group_amount_owed
from db.amoutowed import get_user_id

class TotalGroupAmountAPI(Resource):
    @jwt_required()
    def get(self, group_id):
        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        if not user_id:
            return jsonify({"message": "User not found"}), 404

        debts = get_group_debts(group_id,user_id)
        results = []
        for debt in debts:
            debtor_id = debt[0]
            creditor_id = debt[1]
            debtor_name = debt[2]
            creditor_name = debt[3]
            total_owed = float(debt[4])
            
            if user_id in [debtor_id, creditor_id]: 
                relationship = "owe" if debtor_id == user_id else "owed"
                partner_id = creditor_id if relationship == "owe" else debtor_id
                partner_name = creditor_name if relationship == "owe" else debtor_name
                results.append({
                    "relationship": relationship,
                    "amount": total_owed,
                    "partner_id": partner_id,
                    "partner_name": partner_name
                })

        return jsonify(results)

class TotalGroupAmountAPIbyID(Resource):
    @jwt_required()
    def get(self, group_id, friend_id):
        current_user_username = get_jwt_identity()['username']
        user_id = get_user_id(current_user_username)
        if not user_id:
            return jsonify({"message": "User not found"}), 404
        print("user_id:",user_id)
        print("friend_id:",friend_id)
        result1 = calculate_group_amount_owed(group_id, user_id, friend_id)
        result2 = calculate_group_amount_owed(group_id, friend_id, user_id)
        print("Result1:",result1)
        print("Result2:",result2)
        net_amount =  result1 - result2 
        message = f"You owe {abs(net_amount)}" if net_amount < 0 else f"You are owed {net_amount}"
        return jsonify({"message": message, "net_amount": net_amount})
