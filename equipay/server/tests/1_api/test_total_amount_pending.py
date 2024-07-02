import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.total_amount_pending import NetAmountOwedAPI

class TestNetAmountOwedAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(NetAmountOwedAPI, '/net_amount_owed')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.total_amount_pending.get_user_id')
    @patch('src.api.total_amount_pending.calculate_individual_total_owed')
    @patch('src.api.total_amount_pending.calculate_group_total_owed')
    def test_net_amount_owed_success(self, mock_calculate_group_total_owed, mock_calculate_individual_total_owed, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_calculate_individual_total_owed.return_value = 50.0
        mock_calculate_group_total_owed.return_value = 100.0

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/net_amount_owed', headers=headers)

        expected_response = {"total": 150.0}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.total_amount_pending.get_user_id')
    def test_net_amount_owed_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/net_amount_owed', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.total_amount_pending.get_user_id')
    @patch('src.api.total_amount_pending.calculate_individual_total_owed')
    @patch('src.api.total_amount_pending.calculate_group_total_owed')
    def test_net_amount_owed_no_debts(self, mock_calculate_group_total_owed, mock_calculate_individual_total_owed, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_calculate_individual_total_owed.return_value = 0.0
        mock_calculate_group_total_owed.return_value = 0.0

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/net_amount_owed', headers=headers)

        expected_response = {"total": 0.0}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

if __name__ == '__main__':
    unittest.main()
