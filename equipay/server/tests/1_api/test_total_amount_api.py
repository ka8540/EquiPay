import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.total_amount_api import TotalAmountAPI, TotalAmountAPIbyID

class TestTotalAmountAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(TotalAmountAPI, '/total_amount')
        self.api.add_resource(TotalAmountAPIbyID, '/total_amount/<int:friend_id>')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.total_amount_api.get_user_id')
    @patch('src.api.total_amount_api.get_user_debts')
    def test_total_amount_success(self, mock_get_user_debts, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_user_debts.return_value = [
            (2, 'Friend1', 50.0),
            (3, 'Friend2', -25.0)
        ]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_amount', headers=headers)

        expected_response = [
            {"friend_id": 2, "friend_name": "Friend1", "net_amount": 50.0},
            {"friend_id": 3, "friend_name": "Friend2", "net_amount": -25.0}
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.total_amount_api.get_user_id')
    def test_total_amount_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_amount', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.total_amount_api.exec_get_one')
    @patch('src.api.total_amount_api.calculate_amount_owed')
    def test_total_amount_by_id_success(self, mock_calculate_amount_owed, mock_exec_get_one):
        mock_exec_get_one.return_value = [1]
        mock_calculate_amount_owed.side_effect = [100.0, 50.0]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_amount/2', headers=headers)

        expected_response = {
            "message": "You owe 50.0",
            "net_amount": -50.0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.total_amount_api.exec_get_one')
    @patch('src.api.total_amount_api.calculate_amount_owed')
    def test_total_amount_by_id_user_owes(self, mock_calculate_amount_owed, mock_exec_get_one):
        mock_exec_get_one.return_value = [1]
        mock_calculate_amount_owed.side_effect = [50.0, 100.0]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_amount/2', headers=headers)

        expected_response = {
            "message": "You are owed 50.0",
            "net_amount": 50.0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.total_amount_api.exec_get_one')
    def test_total_amount_by_id_user_not_found(self, mock_exec_get_one):
        mock_exec_get_one.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/total_amount/2', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

if __name__ == '__main__':
    unittest.main()
