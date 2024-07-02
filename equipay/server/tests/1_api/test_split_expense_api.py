import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.split_expense_api import SplitExpenseTwoApi

class TestSplitExpenseTwoApi(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(SplitExpenseTwoApi, '/split_expense')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.split_expense_api.split_expense_')
    @patch('src.api.split_expense_api.get_user_id')
    @patch('src.api.split_expense_api.get_firstname_by_id')
    @patch('src.api.split_expense_api.exec_commit')
    def test_split_expense_success(self, mock_exec_commit, mock_get_firstname_by_id, mock_get_user_id, mock_split_expense):
        mock_split_expense.return_value = True
        mock_get_user_id.return_value = 1
        mock_get_firstname_by_id.side_effect = ['User1', 'Friend1', 'Friend2']

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [2, 3],
            'include_self': True,
            'description': 'Dinner'
        }
        response = self.client.post('/split_expense', headers=headers, json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Expense added and logged successfully."})

    @patch('src.api.split_expense_api.split_expense_')
    def test_split_expense_failure(self, mock_split_expense):
        mock_split_expense.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [2, 3],
            'include_self': True,
            'description': 'Dinner'
        }
        response = self.client.post('/split_expense', headers=headers, json=data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Failed to split expense."})

    @patch('src.api.split_expense_api.split_expense_')
    @patch('src.api.split_expense_api.get_user_id')
    @patch('src.api.split_expense_api.get_firstname_by_id')
    @patch('src.api.split_expense_api.exec_commit')
    def test_split_expense_logging(self, mock_exec_commit, mock_get_firstname_by_id, mock_get_user_id, mock_split_expense):
        mock_split_expense.return_value = True
        mock_get_user_id.return_value = 1
        mock_get_firstname_by_id.side_effect = ['User1', 'Friend1', 'Friend2']

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [2, 3],
            'include_self': True,
            'description': 'Dinner'
        }
        self.client.post('/split_expense', headers=headers, json=data)

        # Check if exec_commit was called the correct number of times
        self.assertEqual(mock_exec_commit.call_count, 3)

        # Check if exec_commit was called with the correct parameters
        expected_calls = [
            ((f"INSERT INTO ActivityLog (UserID, ActionType, Details) VALUES (%s, %s, %s)", 
             (1, 'Added Expense', "User1 added an expense of $100.0 for 'Dinner'.")),),
            ((f"INSERT INTO ActivityLog (UserID, ActionType, Details) VALUES (%s, %s, %s)", 
             (2, 'Incurred Debt', "Friend1 owes User1 $33.33 for 'Dinner'.")),),
            ((f"INSERT INTO ActivityLog (UserID, ActionType, Details) VALUES (%s, %s, %s)", 
             (3, 'Incurred Debt', "Friend2 owes User1 $33.33 for 'Dinner'.")),)
        ]
        mock_exec_commit.assert_has_calls(expected_calls, any_order=True)

if __name__ == '__main__':
    unittest.main()
