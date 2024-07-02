import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.additional_settings_api import DeleteAccountApi
from flask_bcrypt import Bcrypt

class TestDeleteAccountApi(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.bcrypt = Bcrypt(self.app)
        self.api.add_resource(DeleteAccountApi, '/delete_account', resource_class_args=(self.bcrypt,))
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.additional_settings_api.get_username')
    @patch('src.api.additional_settings_api.delete_account')
    def test_delete_account_success(self, mock_delete_account, mock_get_username):
        mock_get_username.return_value = 'testuser'
        mock_delete_account.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}', 'session_key': 'valid_session_key'}
        response = self.client.post('/delete_account', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Account is Deleted Successfully "})

    @patch('src.api.additional_settings_api.get_username')
    def test_delete_account_missing_session_key(self, mock_get_username):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.post('/delete_account', headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Missing session key"})

    @patch('src.api.additional_settings_api.get_username')
    def test_delete_account_invalid_session_key(self, mock_get_username):
        mock_get_username.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}', 'session_key': 'invalid_session_key'}
        response = self.client.post('/delete_account', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Invalid session key"})

    @patch('src.api.additional_settings_api.get_username')
    @patch('src.api.additional_settings_api.delete_account')
    def test_delete_account_failure(self, mock_delete_account, mock_get_username):
        mock_get_username.return_value = 'testuser'
        mock_delete_account.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}', 'session_key': 'valid_session_key'}
        response = self.client.post('/delete_account', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Failed to Delete Account"})

if __name__ == '__main__':
    unittest.main()
