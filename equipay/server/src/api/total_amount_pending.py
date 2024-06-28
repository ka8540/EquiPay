from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.total import calculate_individual_total_owed, calculate_group_total_owed
from db.amoutowed import get_user_id

class NetAmountOwedAPI(Resource):
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        user_id = get_user_id(user_identity['username'])
        
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        individual_owed = calculate_individual_total_owed(user_id) or 0
        group_owed = calculate_group_total_owed(user_id) or 0
        print("Indi:",individual_owed)
        print("Group:",group_owed)
        total = individual_owed + group_owed
        return jsonify({
            "total": total
        })
