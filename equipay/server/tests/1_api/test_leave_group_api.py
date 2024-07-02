import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.leave_group_api import LeaveGroupAPI

class TestLeaveGroupAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(LeaveGroupAPI, '/leave_group/<int:group_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.leave_group_api.get_user_id')
    @patch('src.api.leave_group_api.leave_group')
    def test_leave_group_success(self, mock_leave_group, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_leave_group.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/leave_group/1', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {"message": "Leaving group Successfully"})

    @patch('src.api.leave_group_api.get_user_id')
    def test_leave_group_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/leave_group/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.get_json(), {"message": "User not found"})

    @patch('src.api.leave_group_api.get_user_id')
    @patch('src.api.leave_group_api.leave_group')
    def test_leave_group_failure(self, mock_leave_group, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_leave_group.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.put('/leave_group/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.get_json(), {"error:": "Error Leaving Group"})

if __name__ == '__main__':
    unittest.main()
