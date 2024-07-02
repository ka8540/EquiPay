import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.group_api import GroupMembersAPI, GroupNameByIdAPI

class TestGroupAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(GroupMembersAPI, '/group_members/<int:group_id>')
        self.api.add_resource(GroupNameByIdAPI, '/group_name/<int:group_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.group_api.get_user_id')
    @patch('src.api.group_api.get_group_members_by_group_id')
    def test_get_group_members_success(self, mock_get_group_members_by_group_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_group_members_by_group_id.return_value = [{'username': 'member1'}, {'username': 'member2'}]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_members/1', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'username': 'member1'}, {'username': 'member2'}])

    @patch('src.api.group_api.get_user_id')
    @patch('src.api.group_api.get_group_members_by_group_id')
    def test_get_group_members_no_members(self, mock_get_group_members_by_group_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_group_members_by_group_id.return_value = []

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_members/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "No members found in the group"})

    @patch('src.api.group_api.get_user_id')
    def test_get_group_members_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_members/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.group_api.get_user_id')
    @patch('src.api.group_api.get_group_members_by_group_id')
    def test_get_group_members_exception(self, mock_get_group_members_by_group_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_group_members_by_group_id.side_effect = Exception("Database error")

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_members/1', headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "An error occurred while fetching group members", "details": "Database error"})

    @patch('src.api.group_api.get_user_id')
    @patch('src.api.group_api.get_groups_by_group_id')
    def test_get_group_name_success(self, mock_get_groups_by_group_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_groups_by_group_id.return_value = [("Group 1",)]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_name/1', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"group_name": "Group 1"})

    @patch('src.api.group_api.get_user_id')
    @patch('src.api.group_api.get_groups_by_group_id')
    def test_get_group_name_not_found(self, mock_get_groups_by_group_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_groups_by_group_id.return_value = []

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_name/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "No group name found"})

    @patch('src.api.group_api.get_user_id')
    def test_get_group_name_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_name/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.group_api.get_user_id')
    @patch('src.api.group_api.get_groups_by_group_id')
    def test_get_group_name_exception(self, mock_get_groups_by_group_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_groups_by_group_id.side_effect = Exception("Database error")

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_name/1', headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "An error occurred while fetching the group name", "details": "Database error"})

if __name__ == '__main__':
    unittest.main()
