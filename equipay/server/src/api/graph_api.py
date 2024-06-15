from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id 
from db.graph import get_graph_values  # Renamed to reflect broader usage

class GraphAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()['username']
        user_id = get_user_id(current_user)
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        graph_values = get_graph_values(user_id)
        if not graph_values:
            return make_response(jsonify({"message": "Graph data is empty"}), 404)
        
        return jsonify(graph_values)
