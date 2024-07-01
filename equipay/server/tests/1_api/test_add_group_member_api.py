import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.add_group_members_api import AddGroupMembersAPI

class TestAddGroupMembersAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(AddGroupMembersAPI, '/add_group_member/<int:group_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.add_group_members_api.get_jwt_identity')
    @patch('src.api.add_group_members_api.get_user_id')
    @patch('src.api.add_group_members_api.check_total_members')
    @patch('src.api.add_group_members_api.check_member')
    @patch('src.api.add_group_members_api.add_member_in_group')
    def test_add_member_success(self, mock_add_member_in_group, mock_check_member, mock_check_total_members, mock_get_user_id, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_user_id.return_value = 1
        mock_check_total_members.return_value = True
        mock_check_member.return_value = True
        mock_add_member_in_group.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_group_member/1', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Success": "Added User Successfully"})

    @patch('src.api.add_group_members_api.get_jwt_identity')
    @patch('src.api.add_group_members_api.get_user_id')
    @patch('src.api.add_group_members_api.check_total_members')
    @patch('src.api.add_group_members_api.check_member')
    @patch('src.api.add_group_members_api.add_member_in_group')
    def test_user_not_found(self, mock_add_member_in_group, mock_check_member, mock_check_total_members, mock_get_user_id, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_group_member/1', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.add_group_members_api.get_jwt_identity')
    @patch('src.api.add_group_members_api.get_user_id')
    @patch('src.api.add_group_members_api.check_total_members')
    @patch('src.api.add_group_members_api.check_member')
    @patch('src.api.add_group_members_api.add_member_in_group')
    def test_total_members_limit_exceeded(self, mock_add_member_in_group, mock_check_member, mock_check_total_members, mock_get_user_id, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_user_id.return_value = 1
        mock_check_total_members.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_group_member/1', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Total Members Limit Exceeded!!"})

    @patch('src.api.add_group_members_api.get_jwt_identity')
    @patch('src.api.add_group_members_api.get_user_id')
    @patch('src.api.add_group_members_api.check_total_members')
    @patch('src.api.add_group_members_api.check_member')
    @patch('src.api.add_group_members_api.add_member_in_group')
    def test_member_already_exists(self, mock_add_member_in_group, mock_check_member, mock_check_total_members, mock_get_user_id, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_user_id.return_value = 1
        mock_check_total_members.return_value = True
        mock_check_member.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_group_member/1', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {"message": "Member Already exist"})

    @patch('src.api.add_group_members_api.get_jwt_identity')
    @patch('src.api.add_group_members_api.get_user_id')
    @patch('src.api.add_group_members_api.check_total_members')
    @patch('src.api.add_group_members_api.check_member')
    @patch('src.api.add_group_members_api.add_member_in_group')
    def test_error_adding_user(self, mock_add_member_in_group, mock_check_member, mock_check_total_members, mock_get_user_id, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = {'username': 'testuser'}
        mock_get_user_id.return_value = 1
        mock_check_total_members.return_value = True
        mock_check_member.return_value = True
        mock_add_member_in_group.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/add_group_member/1', json={'friend_id': 2}, headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Error Adding the User"})

if __name__ == '__main__':
    unittest.main()
