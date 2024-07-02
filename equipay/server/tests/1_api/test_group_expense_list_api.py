import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.group_expense_list_api import GroupExpensesListAPI

class TestGroupExpensesListAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(GroupExpensesListAPI, '/group_expenses/<int:group_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.group_expense_list_api.get_user_id')
    @patch('src.api.group_expense_list_api.get_group_expenses')
    def test_get_group_expenses_success(self, mock_get_group_expenses, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_group_expenses.return_value = [
            (1, 'Dinner', 100.0, 'John Doe', '2024-07-01', 50.0),
            (2, 'Lunch', 50.0, 'Jane Doe', '2024-07-02', -25.0)
        ]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_expenses/1', headers=headers)

        expected_response = [
            {
                "expense_id": 1,
                "description": "Dinner",
                "total_amount": "100.00",
                "payer_name": "John Doe",
                "date": "2024-07-01",
                "status": "lend",
                "amount": "50.00"
            },
            {
                "expense_id": 2,
                "description": "Lunch",
                "total_amount": "50.00",
                "payer_name": "Jane Doe",
                "date": "2024-07-02",
                "status": "borrowed",
                "amount": "25.00"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.group_expense_list_api.get_user_id')
    def test_get_group_expenses_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_expenses/1', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.group_expense_list_api.get_user_id')
    @patch('src.api.group_expense_list_api.get_group_expenses')
    def test_get_group_expenses_no_expenses(self, mock_get_group_expenses, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_group_expenses.return_value = []

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/group_expenses/1', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

if __name__ == '__main__':
    unittest.main()
