import unittest
from unittest.mock import patch, MagicMock
from src.db.logout import user_logout  

class TestUserFunctions(unittest.TestCase):

    @patch('src.db.logout.exec_commit')
    @patch('src.db.logout.check_session_key')
    def test_user_logout_success(self, mock_check_session_key, mock_exec_commit):
        mock_check_session_key.return_value = True

        kwargs = {'session_key': 'valid_session_key'}
        result, status_code = user_logout(kwargs)

        expected_result = {"message": "User Logout Successfully!"}
        self.assertEqual(result, expected_result)
        self.assertEqual(status_code, 200)
        mock_check_session_key.assert_called_once_with('valid_session_key')
        mock_exec_commit.assert_called_once_with('''UPDATE "user" SET session_key = NULL WHERE session_key = %s;''', ('valid_session_key',))

    @patch('src.db.logout.exec_commit')
    @patch('src.db.logout.check_session_key')
    def test_user_logout_invalid(self, mock_check_session_key, mock_exec_commit):
        mock_check_session_key.return_value = False

        kwargs = {'session_key': 'invalid_session_key'}
        result, status_code = user_logout(kwargs)

        expected_result = {"message": "Invalid User!!"}
        self.assertEqual(result, expected_result)
        self.assertEqual(status_code, 400)
        mock_check_session_key.assert_called_once_with('invalid_session_key')
        mock_exec_commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
