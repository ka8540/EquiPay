import unittest
from unittest.mock import patch, MagicMock
from src.model.user import check_username_and_password, check_password, check_username, check_session_key, generate_session_key, get_username

class TestUserUtils(unittest.TestCase):

    def test_check_username_and_password_correct(self):
        result = check_username_and_password(True, True, 'session_key')
        self.assertEqual(result, ({"message": "Login Creds are Correct", "sessionKey": 'session_key'}, 200))

    def test_check_username_and_password_invalid_password(self):
        result = check_username_and_password(True, False, 'session_key')
        self.assertEqual(result, ("Password Invalid", 411))

    def test_check_username_and_password_incorrect(self):
        result = check_username_and_password(False, False, 'session_key')
        self.assertEqual(result, ("Login Creds are Incorrect", 410))

    def test_check_password_invalid(self):
        result = check_password('username')
        self.assertEqual(result, ("Password Invalid", 411))

    def test_check_password_correct(self):
        result = check_password('')
        self.assertEqual(result, ("Login Creds are Correct", 200))

    def test_check_username_not_exists(self):
        result = check_username(False)
        self.assertIsNone(result)

    @patch('src.model.user.exec_commit')
    def test_check_session_key_valid(self, mock_exec_commit):
        mock_exec_commit.return_value = True
        result = check_session_key('valid_session_key')
        self.assertEqual(result, ({"message": "Valid Session Key"}, 200))
        mock_exec_commit.assert_called_once_with('''SELECT username FROM "user" WHERE session_key = %s;''', ('valid_session_key',))

    @patch('src.model.user.exec_commit')
    def test_check_session_key_invalid(self, mock_exec_commit):
        mock_exec_commit.return_value = False
        result = check_session_key('invalid_session_key')
        self.assertEqual(result, ({"message": "Not a Valid Session Key"}, 401))
        mock_exec_commit.assert_called_once_with('''SELECT username FROM "user" WHERE session_key = %s;''', ('invalid_session_key',))

    @patch('src.model.user.exec_commit')
    def test_check_session_key_not_provided(self, mock_exec_commit):
        result = check_session_key(None)
        self.assertEqual(result, ({"message:": "Session Key not provided"}, 400))
        mock_exec_commit.assert_not_called()

    def test_generate_session_key(self):
        session_key = generate_session_key()
        self.assertEqual(len(session_key), 32)  # 16-byte hex string should be 32 characters

    @patch('src.model.user.exec_get_all')
    def test_get_username_valid(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('username',)]
        result = get_username('valid_session_key')
        self.assertEqual(result, 'username')
        mock_exec_get_all.assert_called_once_with('''SELECT username FROM "user" WHERE session_key = %s;''', ('valid_session_key',))

    @patch('src.model.user.exec_get_all')
    def test_get_username_invalid(self, mock_exec_get_all):
        mock_exec_get_all.return_value = []
        result = get_username('invalid_session_key')
        self.assertIsNone(result)
        mock_exec_get_all.assert_called_once_with('''SELECT username FROM "user" WHERE session_key = %s;''', ('invalid_session_key',))

    @patch('src.model.user.exec_get_all')
    def test_get_username_exception(self, mock_exec_get_all):
        mock_exec_get_all.side_effect = Exception("Database error")
        result = get_username('valid_session_key')
        self.assertIsNone(result)
        mock_exec_get_all.assert_called_once_with('''SELECT username FROM "user" WHERE session_key = %s;''', ('valid_session_key',))

    def test_get_username_no_session_key(self):
        result = get_username(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
