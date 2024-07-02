import unittest
from unittest.mock import patch
from src.utilities.swen_344_db_utils import exec_get_one, exec_get_all
from src.db.activity import get_firstname_by_id, get_items_for_activity

class TestActivityFunctions(unittest.TestCase):

    @patch('src.db.activity.exec_get_one')
    def test_get_firstname_by_id_success(self, mock_exec_get_one):
        mock_exec_get_one.return_value = ['John']
        
        friend_id = 1
        friend_name = get_firstname_by_id(friend_id)

        self.assertEqual(friend_name, 'John')
        mock_exec_get_one.assert_called_once_with('''SELECT firstname FROM "user" WHERE user_id = %s;''', (friend_id,))

    @patch('src.db.activity.exec_get_all')
    def test_get_items_for_activity_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            ('Login', 'User logged in', '2024-07-01 12:00:00'),
            ('Logout', 'User logged out', '2024-07-01 13:00:00')
        ]
        
        user_id = 1
        activities = get_items_for_activity(user_id)

        expected_activities = [
            ('Login', 'User logged in', '2024-07-01 12:00:00'),
            ('Logout', 'User logged out', '2024-07-01 13:00:00')
        ]
        self.assertEqual(activities, expected_activities)
        mock_exec_get_all.assert_called_once_with('''SELECT ActionType, Details, Timestamp FROM ActivityLog WHERE UserID = %s ORDER BY Timestamp DESC;''', (user_id,))

if __name__ == '__main__':
    unittest.main()
