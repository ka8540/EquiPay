import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.contact_list_api import ContactListAPI

class TestContactListAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(ContactListAPI, '/contacts')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.contact_list_api.get_user_id')
    @patch('src.api.contact_list_api.get_contact')
    def test_get_contacts_success(self, mock_get_contact, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_contact.return_value = [('John Doe', '123-456-7890'), ('Jane Doe', '098-765-4321')]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/contacts', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"firstname": "John Doe", "contact": "123-456-7890"},
            {"firstname": "Jane Doe", "contact": "098-765-4321"}
        ])

    @patch('src.api.contact_list_api.get_user_id')
    def test_get_contacts_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/contacts', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

if __name__ == '__main__':
    unittest.main()
