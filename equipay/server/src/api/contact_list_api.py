from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.contact import check_contacts_exist
import json
import urllib.parse
from db.amoutowed import get_user_id

class ContactListAPI(Resource):
    @jwt_required()
    def post(self):
        jwt_user = get_jwt_identity()
        user_id = get_user_id(jwt_user['username'])
        
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)

        contacts_json = request.args.get('contacts')
        
        if not contacts_json:
            return make_response(jsonify({"message": "No contacts provided"}), 400)

        try:
            contacts_json = urllib.parse.unquote(contacts_json)
            contacts_data = json.loads(contacts_json)
            print("Contacts Data:", contacts_data)
        except (json.JSONDecodeError, ValueError):
            return make_response(jsonify({"message": "Invalid JSON format"}), 400)

        matched_contacts = check_contacts_exist(contacts_data)

        if not matched_contacts:
            return make_response(jsonify({"message": "No matching contacts found"}), 201)

        return jsonify(matched_contacts)
