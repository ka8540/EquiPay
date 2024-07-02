import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.group_expense_api import GroupExpenseAPI

class TestGroupExpenseAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(GroupExpenseAPI, '/group_expense/<int:group_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.group_expense_api.split_group_expense')
    def test_split_group_expense_success(self, mock_split_group_expense):
        mock_split_group_expense.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [1, 2, 3],
            'include_self': True,
            'description': 'Dinner'
        }
        response = self.client.post('/group_expense/1', json=data, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Expense split successfully."})

    @patch('src.api.group_expense_api.split_group_expense')
    def test_split_group_expense_failure(self, mock_split_group_expense):
        mock_split_group_expense.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [1, 2, 3],
            'include_self': True,
            'description': 'Dinner'
        }
        response = self.client.post('/group_expense/1', json=data, headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Failed to split expense."})

    def test_split_group_expense_missing_amount(self):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'friend_ids': [1, 2, 3],
            'include_self': True,
            'description': 'Dinner'
        }
        response = self.client.post('/group_expense/1', json=data, headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Amount cannot be blank!', response.json['message']['amount'])

    def test_split_group_expense_missing_friend_ids(self):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'include_self': True,
            'description': 'Dinner'
        }
        response = self.client.post('/group_expense/1', json=data, headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Friend IDs list cannot be blank!', response.json['message']['friend_ids'])

    def test_split_group_expense_missing_include_self(self):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [1, 2, 3],
            'description': 'Dinner'
        }
        response = self.client.post('/group_expense/1', json=data, headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Include self in split cannot be blank!', response.json['message']['include_self'])

    def test_split_group_expense_missing_description(self):
        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {
            'amount': 100.0,
            'friend_ids': [1, 2, 3],
            'include_self': True
        }
        response = self.client.post('/group_expense/1', json=data, headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Description cannot be blank!', response.json['message']['description'])

if __name__ == '__main__':
    unittest.main()
