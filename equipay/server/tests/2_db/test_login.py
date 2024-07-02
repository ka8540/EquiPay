import unittest
from unittest.mock import patch, MagicMock
from src.db.login import list_info_items, check_user_credentials  # Adjust the import based on your project structure

class TestUserFunctions(unittest.TestCase):

    @patch('src.db.login.exec_get_all')
    def test_list_info_items_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            (1, 'testuser1', 'hashed_password1', 'session_key1'),
            (2, 'testuser2', 'hashed_password2', 'session_key2')
        ]
        result = list_info_items()
        expected_result = [
            (1, 'testuser1', 'hashed_password1', 'session_key1'),
            (2, 'testuser2', 'hashed_password2', 'session_key2')
        ]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with('''SELECT * FROM "user" ''')

    @patch('src.db.login.generate_session_key')
    @patch('src.db.login.exec_commit')
    @patch('src.db.login.exec_get_one')
    def test_check_user_credentials_success(self, mock_exec_get_one, mock_exec_commit, mock_generate_session_key):
        mock_bcrypt = MagicMock()
        mock_bcrypt.check_password_hash.return_value = True
        mock_exec_get_one.return_value = ('testuser', 'hashed_password')
        mock_generate_session_key.return_value = 'new_session_key'

        username = 'testuser'
        password = 'correct_password'
        result, status_code = check_user_credentials(mock_bcrypt, username, password)

        expected_result = {"message": "Login Creds are Correct", "sessionKey": 'new_session_key'}
        self.assertEqual(result, expected_result)
        self.assertEqual(status_code, 200)
        mock_exec_get_one.assert_called_once_with('''SELECT username, password FROM "user" WHERE username = %s;''', (username,))
        mock_exec_commit.assert_called_once_with('''UPDATE "user" SET session_key = %s WHERE username = %s;''', ('new_session_key', username))
        mock_bcrypt.check_password_hash.assert_called_once_with('hashed_password', password)

    @patch('src.db.login.exec_get_one')
    def test_check_user_credentials_user_not_found(self, mock_exec_get_one):
        mock_bcrypt = MagicMock()
        mock_exec_get_one.return_value = None

        username = 'nonexistent_user'
        password = 'any_password'
        result, status_code = check_user_credentials(mock_bcrypt, username, password)

        expected_result = {"message": "Login Creds are Incorrect", "sessionKey": None}
        self.assertEqual(result, expected_result)
        self.assertEqual(status_code, 201)
        mock_exec_get_one.assert_called_once_with('''SELECT username, password FROM "user" WHERE username = %s;''', (username,))

if __name__ == '__main__':
    unittest.main()
