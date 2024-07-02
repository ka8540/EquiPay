import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.group_settle_api import DeleteGroupDebtByIdAPI

class TestDeleteGroupDebtByIdAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(DeleteGroupDebtByIdAPI, '/delete_group_debt/<int:group_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.group_settle_api.get_user_id')
    @patch('src.api.group_settle_api.delete_group_debt')
    def test_delete_group_debt_success(self, mock_delete_group_debt, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_delete_group_debt.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {'friend_id': 2, 'amount_owed': 100.0}
        response = self.client.post('/delete_group_debt/1', headers=headers, json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Debt record deleted successfully"})

    @patch('src.api.group_settle_api.get_user_id')
    def test_delete_group_debt_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {'friend_id': 2, 'amount_owed': 100.0}
        response = self.client.post('/delete_group_debt/1', headers=headers, json=data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})

    @patch('src.api.group_settle_api.get_user_id')
    @patch('src.api.group_settle_api.delete_group_debt')
    def test_delete_group_debt_failure(self, mock_delete_group_debt, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_delete_group_debt.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {'friend_id': 2, 'amount_owed': 100.0}
        response = self.client.post('/delete_group_debt/1', headers=headers, json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Failed to delete debt record"})

if __name__ == '__main__':
    unittest.main()
