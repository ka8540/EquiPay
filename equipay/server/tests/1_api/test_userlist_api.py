import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.userlist_api import ListUsersApi
from flask_bcrypt import Bcrypt

class TestListUsersApi(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.bcrypt = Bcrypt(self.app)
        self.jwt = JWTManager(self.app)
        self.api.add_resource(ListUsersApi, '/list_users', resource_class_args=(self.bcrypt,))
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.userlist_api.get_username')
    @patch('src.api.userlist_api.list_info_items')
    def test_list_users_success(self, mock_list_info_items, mock_get_username):
        mock_get_username.return_value = 'testuser'
        mock_list_info_items.return_value = [{'info_item': 'value1'}, {'info_item': 'value2'}]

        headers = {
            'Authorization': f'Bearer {self.get_valid_token()}',
            'session_key': 'valid_session_key'
        }
        response = self.client.get('/list_users', headers=headers)

        expected_response = [{'info_item': 'value1'}, {'info_item': 'value2'}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.userlist_api.get_username')
    def test_list_users_missing_session_key(self, mock_get_username):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/list_users', headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Missing session key"})

    @patch('src.api.userlist_api.get_username')
    def test_list_users_invalid_session_key(self, mock_get_username):
        mock_get_username.return_value = None

        headers = {
            'Authorization': f'Bearer {self.get_valid_token()}',
            'session_key': 'invalid_session_key'
        }
        response = self.client.get('/list_users', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Invalid session key"})

if __name__ == '__main__':
    unittest.main()
