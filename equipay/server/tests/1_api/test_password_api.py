import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.password_api import PasswordApi
from flask_bcrypt import Bcrypt

class TestPasswordApi(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.bcrypt = Bcrypt(self.app)
        self.jwt = JWTManager(self.app)
        self.api.add_resource(PasswordApi, '/password', resource_class_args=(self.bcrypt,))
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.password_api.get_username')
    @patch('src.api.password_api.get_password')
    @patch('src.api.password_api.update_passord')
    def test_password_update_success(self, mock_update_password, mock_get_password, mock_get_username):
        mock_get_username.return_value = 'testuser'
        mock_get_password.return_value = self.bcrypt.generate_password_hash('oldpassword').decode('utf-8')
        mock_update_password.return_value = True

        headers = {
            'Authorization': f'Bearer {self.get_valid_token()}',
            'session_key': 'valid_session_key'
        }
        data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword'
        }
        response = self.client.post('/password', headers=headers, json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Password Updated Sucessfully"})

    @patch('src.api.password_api.get_username')
    def test_missing_session_key(self, mock_get_username):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword'
        }
        response = self.client.post('/password', headers=headers, json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Missing session key"})

    @patch('src.api.password_api.get_username')
    def test_invalid_session_key(self, mock_get_username):
        mock_get_username.return_value = None

        headers = {
            'Authorization': f'Bearer {self.get_valid_token()}',
            'session_key': 'invalid_session_key'
        }
        data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword'
        }
        response = self.client.post('/password', headers=headers, json=data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Invalid session key"})

    @patch('src.api.password_api.get_username')
    @patch('src.api.password_api.get_password')
    def test_incorrect_old_password(self, mock_get_password, mock_get_username):
        mock_get_username.return_value = 'testuser'
        mock_get_password.return_value = None

        headers = {
            'Authorization': f'Bearer {self.get_valid_token()}',
            'session_key': 'valid_session_key'
        }
        data = {
            'old_password': 'wrongoldpassword',
            'new_password': 'newpassword'
        }
        response = self.client.post('/password', headers=headers, json=data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Password is Incorrect"})

if __name__ == '__main__':
    unittest.main()
