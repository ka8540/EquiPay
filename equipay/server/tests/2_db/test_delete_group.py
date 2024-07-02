import unittest
from unittest.mock import patch
from src.utilities.swen_344_db_utils import exec_commit, exec_get_all, exec_get_one
from src.db.delete_group import delete_group1, leave_group, add_member_in_group, check_total_members, check_member  # Adjust the import based on your project structure

class TestGroupFunctions(unittest.TestCase):

    @patch('src.db.delete_group.exec_commit')  # Adjust the patch target based on your project structure
    @patch('src.db.delete_group.exec_get_all')
    def test_delete_group1_success(self, mock_exec_get_all, mock_exec_commit):
        mock_exec_commit.return_value = None
        mock_exec_get_all.return_value = []
        
        user_id = 1
        group_id = 1
        result = delete_group1(user_id, group_id)
        
        self.assertTrue(result)
        mock_exec_commit.assert_called_once_with(
            '''DELETE FROM Groups
            WHERE CreatedBy = %s
            AND GroupID = %s
            AND GroupID IN (
                SELECT GroupID
                FROM GroupMembers
                WHERE UserID = %s
                AND GroupID = %s
                AND IsAdmin = TRUE
            );''', (user_id, group_id, user_id, group_id)
        )
        mock_exec_get_all.assert_called_once_with(
            '''SELECT * FROM Groups
                     WHERE GroupID = %s;''', (group_id,)
        )

    @patch('src.db.delete_group.exec_commit')  # Adjust the patch target based on your project structure
    @patch('src.db.delete_group.exec_get_all')
    def test_leave_group_success(self, mock_exec_get_all, mock_exec_commit):
        mock_exec_commit.return_value = None
        mock_exec_get_all.return_value = []
        
        user_id = 1
        group_id = 1
        result = leave_group(user_id, group_id)
        
        self.assertTrue(result)
        mock_exec_commit.assert_called_once_with(
            '''DELETE FROM GroupMembers WHERE GroupID = %s AND UserID = %s;''', (group_id, user_id)
        )
        mock_exec_get_all.assert_called_once_with(
            '''SELECT MemberID FROM GroupMembers WHERE GroupID = %s and UserID = %s;''', (group_id, user_id)
        )

    @patch('src.db.delete_group.exec_commit')  # Adjust the patch target based on your project structure
    @patch('src.db.delete_group.exec_get_one')
    def test_add_member_in_group_success(self, mock_exec_get_one, mock_exec_commit):
        mock_exec_commit.return_value = None
        mock_exec_get_one.return_value = [1]
        
        group_id = 1
        friend_id = 2
        result = add_member_in_group(group_id, friend_id)
        
        self.assertTrue(result)
        mock_exec_commit.assert_called_once_with(
            '''INSERT INTO GroupMembers (GroupID, UserID) VALUES (%s, %s);''', (group_id, friend_id)
        )
        mock_exec_get_one.assert_called_once_with(
            '''SELECT MemberID FROM GroupMembers WHERE GroupID = %s AND UserID = %s''', (group_id, friend_id)
        )

    @patch('src.db.delete_group.exec_get_all')  # Adjust the patch target based on your project structure
    def test_check_total_members_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [(1,), (2,), (3,)]
        
        group_id = 1
        result = check_total_members(group_id)
        
        self.assertTrue(result)
        mock_exec_get_all.assert_called_once_with(
            '''SELECT UserID FROM GroupMembers WHERE GroupID = %s;''', (group_id,)
        )

    @patch('src.db.delete_group.exec_get_one')  # Adjust the patch target based on your project structure
    def test_check_member_success(self, mock_exec_get_one):
        mock_exec_get_one.return_value = None
        
        group_id = 1
        friend_id = 2
        result = check_member(group_id, friend_id)
        
        self.assertTrue(result)
        mock_exec_get_one.assert_called_once_with(
            '''SELECT MemberID FROM GroupMembers WHERE GroupID = %s AND UserID = %s;''', (group_id, friend_id)
        )

if __name__ == '__main__':
    unittest.main()
