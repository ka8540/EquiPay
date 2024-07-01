import unittest
from unittest.mock import patch

from tests.test_utils import requests
 


class LoginApiTestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5000/login'

    @patch('requests.post')
    def test_successful_login(self, mock_post):
        user_credentials = {
            "username": "testuser",
            "password": "testpassword"
        }

        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "fake_jwt_token_here",
            "sessionKey": "fake_session_key_here"
        }

        mock_post.return_value = mock_response
        response = requests.post(self.BASE_URL, json=user_credentials)

        # Assertions to validate behavior
        mock_post.assert_called_once_with(self.BASE_URL, json=user_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "access_token": "fake_jwt_token_here",
            "sessionKey": "fake_session_key_here"
        })

    @patch('requests.post')
    def test_failed_login(self, mock_post):
        user_credentials = {
            "username": "wronguser",
            "password": "wrongpassword"
        }

        mock_response = unittest.mock.Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid credentials"}

        mock_post.return_value = mock_response

        response = requests.post(self.BASE_URL, json=user_credentials)

        mock_post.assert_called_once_with(self.BASE_URL, json=user_credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "Invalid credentials"})


if __name__ == '__main__':
    unittest.main()
