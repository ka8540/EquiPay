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
    @patch('src.api.contact_list_api.check_contacts_exist')
    def test_post_contacts_success(self, mock_check_contacts_exist, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_check_contacts_exist.return_value = [
            {"firstname": "John Doe", "contact": "123-456-7890"},
            {"firstname": "Jane Doe", "contact": "098-765-4321"}
        ]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        contacts_json = '[{"firstname": "John Doe", "contact": "123-456-7890"}, {"firstname": "Jane Doe", "contact": "098-765-4321"}]'
        response = self.client.post('/contacts', headers=headers, query_string={'contacts': contacts_json})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"firstname": "John Doe", "contact": "123-456-7890"},
            {"firstname": "Jane Doe", "contact": "098-765-4321"}
        ])

    @patch('src.api.contact_list_api.get_user_id')
    def test_post_contacts_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        contacts_json = '[{"firstname": "John Doe", "contact": "123-456-7890"}, {"firstname": "Jane Doe", "contact": "098-765-4321"}]'
        response = self.client.post('/contacts', headers=headers, query_string={'contacts': contacts_json})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.contact_list_api.get_user_id')
    def test_post_contacts_invalid_json_format(self, mock_get_user_id):
        mock_get_user_id.return_value = 1

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        invalid_contacts_json = 'invalid-json'
        response = self.client.post('/contacts', headers=headers, query_string={'contacts': invalid_contacts_json})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid JSON format"})

if __name__ == '__main__':
    unittest.main()
