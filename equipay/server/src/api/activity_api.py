from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id 
from db.activity import get_items_for_activity

class ActivityAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()['username']
        user_id = get_user_id(current_user)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)

        result = get_items_for_activity(user_id)
        if not result:
            return jsonify({"message": "No Logs Found", "logs": []})
        logs = [{"actiontype": log[0], "details": log[1], "timestamp": log[2].isoformat()} for log in result]
        return jsonify({"logs": logs})
