import unittest
from unittest.mock import patch
from src.db.friends import existing_friend, get_pending_friend_requests, get_friend_requests, update_friend_request_status, add_friend_request  # Adjust the import based on your project structure

class TestFriendsFunctions(unittest.TestCase):

    @patch('src.db.friends.exec_get_one')  # Adjust the patch target based on your project structure
    @patch('src.db.friends.exec_get_all')
    def test_existing_friend_success(self, mock_exec_get_all, mock_exec_get_one):
        mock_exec_get_one.return_value = [1]
        mock_exec_get_all.return_value = [1]
        
        username = "testuser"
        friend_id = 2
        result = existing_friend(username, friend_id)
        
        self.assertTrue(result)
        mock_exec_get_one.assert_called_once_with(
            '''SELECT user_id FROM "user" WHERE username = %s;''', (username,)
        )
        mock_exec_get_all.assert_called_once_with(
            '''SELECT 1 FROM Friends WHERE (UserID = %s AND FriendUserID = %s);''', (1, friend_id)
        )

    @patch('src.db.friends.exec_get_all')  # Adjust the patch target based on your project structure
    def test_get_friend_requests_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [(1, 'Friend1'), (2, 'Friend2')]
        
        username = "testuser"
        result = get_friend_requests(username)
        
        expected_result = [(1, 'Friend1'), (2, 'Friend2')]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            '''
    SELECT u.user_id, u.firstname
    FROM Friends f
    JOIN "user" u ON u.user_id = f.FriendUserID
    WHERE f.UserID = (SELECT user_id FROM "user" WHERE username = %s)
    AND f.Status = 'accepted'
    UNION
    SELECT u.user_id, u.firstname
    FROM Friends f
    JOIN "user" u ON u.user_id = f.UserID
    WHERE f.FriendUserID = (SELECT user_id FROM "user" WHERE username = %s)
    AND f.Status = 'accepted';
    ''', (username, username)
        )


    @patch('src.db.friends.exec_commit')  # Adjust the patch target based on your project structure
    @patch('src.db.friends.exec_get_one')
    def test_add_friend_request_success(self, mock_exec_get_one, mock_exec_commit):
        mock_exec_get_one.return_value = [1]
        
        username = "testuser"
        friend_id = 2
        result = add_friend_request(username, friend_id)
        
        self.assertTrue(result)
        mock_exec_get_one.assert_called_once_with(
            '''SELECT user_id FROM "user" WHERE username = %s;''', (username,)
        )
        mock_exec_commit.assert_called_once_with(
            "INSERT INTO Friends (UserID, FriendUserID, Status) VALUES (%s, %s, 'pending')", (1, friend_id)
        )

if __name__ == '__main__':
    unittest.main()
