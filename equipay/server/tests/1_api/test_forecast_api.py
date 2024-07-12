import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
import json

from src.api.forecast_api import ForecastAPI  # Update this to your actual module name

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
api = Api(app)
jwt = JWTManager(app)

api.add_resource(ForecastAPI, '/forecast')

class ForecastAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        with app.app_context():
            self.access_token = create_access_token(identity={'username': 'testuser'})

    @patch('src.api.forecast_api.jwt_required', return_value=lambda fn: fn)  # Update to your actual module path
    @patch('src.api.forecast_api.get_jwt_identity', return_value={'username': 'testuser'})  # Update to your actual module path
    @patch('src.api.forecast_api.get_user_id', return_value=1)  # Update to your actual module path
    @patch('src.api.forecast_api.fetch_user_expenses', return_value=[{'Amount': 100, 'Date': '2024-05-01'}, {'Amount': 150, 'Date': '2024-06-01'}])  # Mocked expenses data
    def test_forecast_get_success(self, mock_fetch_user_expenses, mock_get_user_id, mock_get_jwt_identity, mock_jwt_required):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/forecast', headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('forecast', response_data)
        self.assertIsInstance(response_data['forecast'], dict)

    @patch('src.api.forecast_api.jwt_required', return_value=lambda fn: fn)  # Update to your actual module path
    @patch('src.api.forecast_api.get_jwt_identity', return_value={'username': 'testuser'})  # Update to your actual module path
    @patch('src.api.forecast_api.get_user_id', return_value=None)  # Simulate user not found
    def test_forecast_user_not_found(self, mock_get_user_id, mock_get_jwt_identity, mock_jwt_required):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/forecast', headers=headers)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'User not found')

    @patch('src.api.forecast_api.jwt_required', return_value=lambda fn: fn)  # Update to your actual module path
    @patch('src.api.forecast_api.get_jwt_identity', return_value={'username': 'testuser'})  # Update to your actual module path
    @patch('src.api.forecast_api.get_user_id', return_value=1)  # Update to your actual module path
    @patch('src.api.forecast_api.fetch_user_expenses', return_value=[])  # Simulate no expenses found
    def test_forecast_no_expenses(self, mock_fetch_user_expenses, mock_get_user_id, mock_get_jwt_identity, mock_jwt_required):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/forecast', headers=headers)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'No expenses found for the user')

if __name__ == '__main__':
    unittest.main()
