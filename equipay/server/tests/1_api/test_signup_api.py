import unittest
from unittest.mock import patch
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from src.api.signup_api import SignUpApi

class SignUpApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.bcrypt = Bcrypt(self.app)
        self.api = Api(self.app)
        self.api.add_resource(SignUpApi, '/signup', resource_class_args=[self.bcrypt])
        self.client = self.app.test_client()  
        self.client.testing = True

    @patch('src.api.signup_api.user_signup')
    def test_successful_signup(self, mock_user_signup):
        user_data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "firstname": "New",
            "lastname": "User",
            "contact_number": "1234567890"
        }
        mock_user_signup.return_value = ({"message": "User created successfully"}, 201)
        response = self.client.post('/signup', json=user_data)
        mock_user_signup.assert_called_once_with(self.bcrypt, **user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "User created successfully"})

    @patch('src.api.signup_api.user_signup')
    def test_failed_signup(self, mock_user_signup):
        user_data = {
            "username": "existinguser",
            "password": "password123",
            "email": "existing@example.com",
            "firstname": "Existing",
            "lastname": "User",
            "contact_number": "1234567890"
        }
        mock_user_signup.return_value = ({"message": "User already exists"}, 409)
        response = self.client.post('/signup', json=user_data)
        mock_user_signup.assert_called_once_with(self.bcrypt, **user_data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json(), {"message": "User already exists"})

if __name__ == '__main__':
    unittest.main()
