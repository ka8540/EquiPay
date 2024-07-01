import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.api.activity_api import ActivityAPI

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'  # Ensure you have a secret key for JWT
api = Api(app)
jwt = JWTManager(app)

api.add_resource(ActivityAPI, '/activity')

class ActivityApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        with app.app_context():
            self.access_token = create_access_token(identity={'username': 'testuser'})

    @patch('src.api.activity_api.get_jwt_identity', return_value={'username': 'testuser'})
    @patch('src.api.activity_api.get_user_id', return_value=1)
    @patch('src.api.activity_api.get_items_for_activity')
    def test_activity_get_success(self, mock_get_items_for_activity, mock_get_user_id, mock_get_jwt_identity):
        mock_get_items_for_activity.return_value = [
            ('action1', 'details1', datetime.datetime(2023, 1, 1, 12, 0)),
            ('action2', 'details2', datetime.datetime(2023, 1, 2, 13, 0)),
        ]
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/activity', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "logs": [
                {"actiontype": "action1", "details": "details1", "timestamp": "2023-01-01T12:00:00"},
                {"actiontype": "action2", "details": "details2", "timestamp": "2023-01-02T13:00:00"}
            ]
        })

    @patch('src.api.activity_api.get_jwt_identity', return_value={'username': 'testuser'})
    @patch('src.api.activity_api.get_user_id', return_value=None)
    def test_activity_get_user_not_found(self, mock_get_user_id, mock_get_jwt_identity):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/activity', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('src.api.activity_api.get_jwt_identity', return_value={'username': 'testuser'})
    @patch('src.api.activity_api.get_user_id', return_value=1)
    @patch('src.api.activity_api.get_items_for_activity', return_value=[])
    def test_activity_get_no_logs(self, mock_get_items_for_activity, mock_get_user_id, mock_get_jwt_identity):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/activity', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "No Logs Found", "logs": []})

if __name__ == '__main__':
    unittest.main()
