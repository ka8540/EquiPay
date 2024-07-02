import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.logout_api import LogoutAPI

class TestLogoutAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to your JWT secret key
        self.api = Api(self.app)
        self.jwt = JWTManager(self.app)
        self.api.add_resource(LogoutAPI, '/logout')
        self.client = self.app.test_client()
        with self.app.app_context():
            self.access_token = create_access_token(identity='testuser')

    @patch('src.api.logout_api.user_logout')
    @patch('src.api.logout_api.get_jwt_identity')
    def test_logout_success(self, mock_get_jwt_identity, mock_user_logout):
        mock_get_jwt_identity.return_value = 'testuser'
        mock_user_logout.return_value = {"message": "User Logout Successfully!"}, 200

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.client.post('/logout', json={'session_key': 's3ss10nk3y'}, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User Logout Successfully!"})
        mock_get_jwt_identity.assert_called_once()
        mock_user_logout.assert_called_once_with({'session_key': 's3ss10nk3y'})

    @patch('src.api.logout_api.user_logout')
    @patch('src.api.logout_api.get_jwt_identity')
    def test_logout_invalid_user(self, mock_get_jwt_identity, mock_user_logout):
        mock_get_jwt_identity.return_value = 'testuser'
        mock_user_logout.return_value = {"message": "Invalid User!!"}, 400

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.client.post('/logout', json={'session_key': 'invalid_session_key'}, headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid User!!"})
        mock_get_jwt_identity.assert_called_once()
        mock_user_logout.assert_called_once_with({'session_key': 'invalid_session_key'})

if __name__ == '__main__':
    unittest.main()
