import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.settle_api import DebtsByFriendAPI, DeleteDebtAPI

class TestDebtsByFriendAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(DebtsByFriendAPI, '/debts/<int:friend_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.settle_api.get_user_id')
    @patch('src.api.settle_api.get_debts_by_friend')
    def test_get_debts_success(self, mock_get_debts_by_friend, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_debts_by_friend.return_value = [{'debt_id': 1, 'amount': 50.0}]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/debts/2', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'debt_id': 1, 'amount': 50.0}])

    @patch('src.api.settle_api.get_user_id')
    def test_get_debts_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/debts/2', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.settle_api.get_user_id')
    @patch('src.api.settle_api.get_debts_by_friend')
    def test_get_debts_no_debts_found(self, mock_get_debts_by_friend, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_debts_by_friend.return_value = []

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/debts/2', headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "No debts found"})


class TestDeleteDebtAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(DeleteDebtAPI, '/delete_debt')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.settle_api.get_user_id')
    @patch('src.api.settle_api.get_firstname_by_id')
    @patch('src.api.settle_api.delete_debt')
    @patch('src.api.settle_api.exec_commit')
    def test_delete_debt_success(self, mock_exec_commit, mock_delete_debt, mock_get_firstname_by_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_firstname_by_id.side_effect = ['User1', 'Friend1']
        mock_delete_debt.return_value = True

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {'friend_id': 2}
        response = self.client.post('/delete_debt', headers=headers, json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Debt record deleted successfully"})

    @patch('src.api.settle_api.get_user_id')
    @patch('src.api.settle_api.get_firstname_by_id')
    @patch('src.api.settle_api.delete_debt')
    def test_delete_debt_failure(self, mock_delete_debt, mock_get_firstname_by_id, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_firstname_by_id.side_effect = ['User1', 'Friend1']
        mock_delete_debt.return_value = False

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        data = {'friend_id': 2}
        response = self.client.post('/delete_debt', headers=headers, json=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "No Debt Record"})


if __name__ == '__main__':
    unittest.main()
