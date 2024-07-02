import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from src.api.graph_api import GraphAPI

class TestGraphAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.api.add_resource(GraphAPI, '/graph')
        self.client = self.app.test_client()

    def get_valid_token(self):
        with self.app.app_context():
            return create_access_token(identity={'username': 'testuser'})

    @patch('src.api.graph_api.get_user_id')
    @patch('src.api.graph_api.get_graph_values')
    def test_get_graph_success(self, mock_get_graph_values, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_graph_values.return_value = [{'label': 'Test', 'value': 100}]

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/graph', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'label': 'Test', 'value': 100}])

    @patch('src.api.graph_api.get_user_id')
    @patch('src.api.graph_api.get_graph_values')
    def test_get_graph_empty(self, mock_get_graph_values, mock_get_user_id):
        mock_get_user_id.return_value = 1
        mock_get_graph_values.return_value = []

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/graph', headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Graph data is empty"})

    @patch('src.api.graph_api.get_user_id')
    def test_get_graph_user_not_found(self, mock_get_user_id):
        mock_get_user_id.return_value = None

        headers = {'Authorization': f'Bearer {self.get_valid_token()}'}
        response = self.client.get('/graph', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

if __name__ == '__main__':
    unittest.main()
