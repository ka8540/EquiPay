import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.group_total_expense_api import TotalGroupAmountAPI, TotalGroupAmountAPIbyID

class TestTotalGroupAmountAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(TotalGroupAmountAPI, '/total_group_amount/<int:group_id>')
        self.api.add_resource(TotalGroupAmountAPIbyID, '/total_group_amount/<int:group_id>/<int:friend_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.group_total_expense_api.get_user_id')
    @patch('src.api.group_total_expense_api.get_group_debts')
    def test_total_group_amount_success(self, mock_get_group_debts, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_group_debts.return_value = [
            (1, 2, 'User1', 'User2', 100.0),
            (2, 1, 'User2', 'User1', 50.0)
        ]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_group_amount/1', headers=headers)

        expected_response = [
            {"relationship": "owe", "amount": 100.0, "partner_id": 2, "partner_name": "User2"},
            {"relationship": "owed", "amount": 50.0, "partner_id": 2, "partner_name": "User2"}
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.group_total_expense_api.get_user_id')
    def test_total_group_amount_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_group_amount/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.group_total_expense_api.get_user_id')
    @patch('src.api.group_total_expense_api.calculate_group_amount_owed')
    def test_total_group_amount_by_id_success(self, mock_calculate_group_amount_owed, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_calculate_group_amount_owed.side_effect = [100.0, 50.0]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_group_amount/1/2', headers=headers)

        expected_response = {
            "message": "You are owed 50.0",
            "net_amount": 50.0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.group_total_expense_api.get_user_id')
    def test_total_group_amount_by_id_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_group_amount/1/2', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

if __name__ == '__main__':
    unittest.main()
