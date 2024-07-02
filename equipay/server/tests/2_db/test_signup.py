import unittest
from unittest.mock import patch, MagicMock
from src.db.signup import user_signup

class TestUserSignup(unittest.TestCase):

    @patch('src.db.signup.exec_get_all')
    @patch('src.db.signup.exec_commit')
    def test_user_signup_success(self, mock_exec_commit, mock_exec_get_all):
        # Mock bcrypt password hash generation
        mock_bcrypt = MagicMock()
        mock_bcrypt.generate_password_hash.return_value = MagicMock(decode=MagicMock(return_value='hashed_password'))
        
        # Mock exec_get_all to return an empty list, indicating user does not exist
        mock_exec_get_all.return_value = []

        # Define input parameters
        kwargs = {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
            'email': 'johndoe@example.com',
            'contact_number': '1234567890'
        }

        # Call the function
        result, status_code = user_signup(mock_bcrypt, **kwargs)

        # Assertions
        self.assertEqual(result, {"message": "User registered successfully"})
        self.assertEqual(status_code, 200)
        mock_exec_get_all.assert_called_once_with('SELECT username FROM "user" WHERE username = %s;', ('johndoe',))
        mock_exec_commit.assert_called_once_with(
            'INSERT INTO "user" (firstname, lastname, username, password, email,contact_number) VALUES (%s, %s, %s, %s, %s,%s);',
            ('John', 'Doe', 'johndoe', 'hashed_password', 'johndoe@example.com', '1234567890')
        )

    @patch('src.db.signup.exec_get_all')
    @patch('src.db.signup.exec_commit')
    def test_user_signup_user_exists(self, mock_exec_commit, mock_exec_get_all):
        # Mock exec_get_all to return a list, indicating user exists
        mock_exec_get_all.return_value = [('johndoe',)]

        # Define input parameters
        kwargs = {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
            'email': 'johndoe@example.com',
            'contact_number': '1234567890'
        }

        # Call the function
        mock_bcrypt = MagicMock()
        result, status_code = user_signup(mock_bcrypt, **kwargs)

        # Assertions
        self.assertEqual(result, {"message": "User already exists"})
        self.assertEqual(status_code, 409)
        mock_exec_get_all.assert_called_once_with('SELECT username FROM "user" WHERE username = %s;', ('johndoe',))
        mock_exec_commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
