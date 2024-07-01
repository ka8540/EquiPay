import unittest
from unittest.mock import patch
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.api.account_api import AccountApi, FriendNameAPI

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(AccountApi, '/account', resource_class_args=[bcrypt])
api.add_resource(FriendNameAPI, '/friend_name/<int:friend_id>')

class AccountApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        with app.app_context():
            self.access_token = create_access_token(identity='testuser')

    @patch('src.api.account_api.jwt_required', return_value=lambda fn: fn)
    @patch('src.api.account_api.get_username', return_value='testuser')
    @patch('src.api.account_api.list_user_detail', return_value={"username": "testuser", "email": "test@example.com"})
    def test_account_get_success(self, mock_list_user_detail, mock_get_username, mock_jwt_required):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'session_key': 'valid_session_key'
        }
        response = self.client.get('/account', headers=headers)
        print("GET /account response data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"username": "testuser", "email": "test@example.com"})

    @patch('src.api.account_api.jwt_required', return_value=lambda fn: fn)
    @patch('src.api.account_api.get_username', return_value='testuser')
    @patch('src.api.account_api.update_user_detail', return_value=True)
    def test_account_put_success(self, mock_update_user_detail, mock_get_username, mock_jwt_required):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'session_key': 'valid_session_key'
        }
        response = self.client.put('/account', json={"email": "new@example.com"}, headers=headers)
        print("PUT /account response data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User details updated successfully"})

class FriendNameAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        with app.app_context():
            self.access_token = create_access_token(identity={'username': 'testuser'})

    @patch('src.api.account_api.jwt_required', return_value=lambda fn: fn)
    @patch('src.api.account_api.get_user_id', return_value=1)
    @patch('src.api.account_api.get_firstname_by_id', return_value="John")
    def test_friend_name_success(self, mock_get_firstname_by_id, mock_get_user_id, mock_jwt_required):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/friend_name/2', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"friend_name": "John"})

if __name__ == '__main__':
    unittest.main()
