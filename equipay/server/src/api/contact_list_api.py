# api/contact.py
from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.amoutowed import get_user_id
from db.contact import get_contact

class ContactListAPI(Resource):
    @jwt_required()
    def get(self):
        jwt_user = get_jwt_identity()
        user_id = get_user_id(jwt_user['username'])

        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)

        contacts = get_contact()
        contact_list = [{"firstname": contact[0], "contact": contact[1]} for contact in contacts]

        return make_response(jsonify(contact_list), 200)
