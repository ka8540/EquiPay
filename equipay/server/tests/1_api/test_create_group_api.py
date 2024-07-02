import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.create_group_api import UserGroupsAPI, CreateGroupAPI

class TestUserGroupsAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(UserGroupsAPI, '/user_groups')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.create_group_api.get_user_id')
    @patch('src.api.create_group_api.get_groups_by_user_id')
    def test_get_groups_success(self, mock_get_groups_by_user_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_groups_by_user_id.return_value = [{'group_id': 1, 'group_name': 'Test Group'}]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/user_groups', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'group_id': 1, 'group_name': 'Test Group'}])

    @patch('src.api.create_group_api.get_user_id')
    def test_get_groups_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/user_groups', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.create_group_api.get_user_id')
    @patch('src.api.create_group_api.get_groups_by_user_id')
    def test_get_groups_no_groups_found(self, mock_get_groups_by_user_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_groups_by_user_id.return_value = []

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/user_groups', headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "No groups found"})

    @patch('src.api.create_group_api.get_user_id')
    @patch('src.api.create_group_api.get_groups_by_user_id')
    def test_get_groups_error(self, mock_get_groups_by_user_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_groups_by_user_id.side_effect = Exception('Test exception')

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/user_groups', headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "An error occurred while fetching groups", "details": "Test exception"})

class TestCreateGroupAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(CreateGroupAPI, '/create_group')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.create_group_api.get_user_id')
    @patch('src.api.create_group_api.get_firstname_by_id')
    @patch('src.api.create_group_api.create_group')
    @patch('src.api.create_group_api.exec_commit')
    @patch('src.api.create_group_api.add_group_member')
    def test_create_group_success(self, mock_add_group_member, mock_exec_commit, mock_create_group, mock_get_firstname_by_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_firstname_by_id.return_value = 'TestUser'
        mock_create_group.return_value = 1

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'friend_ids': [2, 3],
            'profile_picture_url': 'http://example.com/image.png',
            'group_name': 'Test Group'
        }
        response = self.client.post('/create_group', json=data, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Group created successfully", "group_id": 1})

    @patch('src.api.create_group_api.get_user_id')
    @patch('src.api.create_group_api.get_firstname_by_id')
    @patch('src.api.create_group_api.create_group')
    def test_create_group_user_not_found(self, mock_create_group, mock_get_firstname_by_id, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'friend_ids': [2, 3],
            'profile_picture_url': 'http://example.com/image.png',
            'group_name': 'Test Group'
        }
        response = self.client.post('/create_group', json=data, headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})

    @patch('src.api.create_group_api.get_user_id')
    @patch('src.api.create_group_api.get_firstname_by_id')
    @patch('src.api.create_group_api.create_group')
    def test_create_group_failure(self, mock_create_group, mock_get_firstname_by_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_firstname_by_id.return_value = 'TestUser'
        mock_create_group.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'friend_ids': [2, 3],
            'profile_picture_url': 'http://example.com/image.png',
            'group_name': 'Test Group'
        }
        response = self.client.post('/create_group', json=data, headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Failed to create group"})

if __name__ == '__main__':
    unittest.main()
