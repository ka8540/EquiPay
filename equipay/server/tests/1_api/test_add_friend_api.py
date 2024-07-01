import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.addfriend_api import AddFriendApi

class TestAddFriendApi(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(AddFriendApi, '/add_friend')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.get_pending_friend_requests')
    def test_get_friend_requests_success(self, mock_get_pending_friend_requests, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_pending_friend_requests.return_value = [{"friend_id": 1, "status": "pending"}]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/add_friend', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"friend_id": 1, "status": "pending"}])

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.get_pending_friend_requests')
    def test_get_friend_requests_failure(self, mock_get_pending_friend_requests, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_pending_friend_requests.side_effect = Exception("Database error")

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/add_friend', headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Database error"})

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.existing_friend')
    @patch('src.api.addfriend_api.add_friend_request')
    def test_post_friend_request_success(self, mock_add_friend_request, mock_existing_friend, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_existing_friend.return_value = False
        mock_add_friend_request.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.post('/add_friend', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Friend request sent successfully"})

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.existing_friend')
    def test_post_friend_request_exists(self, mock_existing_friend, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_existing_friend.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.post('/add_friend', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json, {"message": "Friend request already exists"})

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.existing_friend')
    @patch('src.api.addfriend_api.add_friend_request')
    def test_post_friend_request_failure(self, mock_add_friend_request, mock_existing_friend, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_existing_friend.return_value = False
        mock_add_friend_request.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.post('/add_friend', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Failed to send friend request"})

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.update_friend_request_status')
    def test_put_friend_request_success(self, mock_update_friend_request_status, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_update_friend_request_status.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_friend', json={'friend_id': 2, 'action': 'accept'}, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Friend request updated successfully"})

    @patch('src.api.addfriend_api.get_jwt_identity')
    @patch('src.api.addfriend_api.update_friend_request_status')
    def test_put_friend_request_failure(self, mock_update_friend_request_status, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_update_friend_request_status.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_friend', json={'friend_id': 2, 'action': 'accept'}, headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Failed to update friend request"})

if __name__ == '__main__':
    unittest.main()
