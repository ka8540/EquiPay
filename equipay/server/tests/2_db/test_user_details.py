import unittest
from unittest.mock import patch, MagicMock
from src.db.user_details import (
    list_info_items,
    list_user_detail,
    verify_session_key,
    update_user_detail,
    get_password,
    update_passord,
    update_user_image_url,
    update_group_image_url,
    profile_picture,
    group_profile_picture,
    check_friendship_and_get_profile_pic,
    delete_account
)

class TestUserDetailsFunctions(unittest.TestCase):

    @patch('src.db.user_details.exec_get_all')
    def test_list_user_detail(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('John', 'Doe', 'johndoe', 'john@example.com')]
        username = 'johndoe'
        result = list_user_detail(username)
        self.assertEqual(result, [{'firstname': 'John', 'lastname': 'Doe', 'username': 'johndoe', 'email': 'john@example.com'}])
        mock_exec_get_all.assert_called_once_with(
            '''SELECT firstname, lastname, username, email FROM "user" WHERE username = %s;''', (username,)
        )

    @patch('src.db.user_details.exec_get_all')
    def test_verify_session_key(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('johndoe',)]
        session_key = 's3ss10nk3y'
        result = verify_session_key(session_key)
        self.assertEqual(result, 'johndoe')
        mock_exec_get_all.assert_called_once_with(
            '''SELECT username FROM user_authentication WHERE session_key = %s;''', (session_key,)
        )

    @patch('src.db.user_details.exec_commit')
    def test_update_user_detail(self, mock_exec_commit):
        username = 'johndoe'
        kwargs = {'email': 'new_email@example.com'}
        result = update_user_detail(username, **kwargs)
        self.assertTrue(result)
        mock_exec_commit.assert_called_once_with(
            'UPDATE "user" SET email = %s WHERE username = %s;', ('new_email@example.com', username)
        )

    @patch('src.db.user_details.exec_get_all')
    @patch('src.db.user_details.bcrypt')
    def test_get_password(self, mock_bcrypt, mock_exec_get_all):
        mock_exec_get_all.return_value = [('hashed_password',)]
        mock_bcrypt.check_password_hash.return_value = True
        username = 'johndoe'
        old_password = 'old_password'
        result = get_password(username, old_password)
        self.assertTrue(result)
        mock_exec_get_all.assert_called_once_with(
            '''SELECT password FROM "user" WHERE username = %s;''', (username,)
        )
        mock_bcrypt.check_password_hash.assert_called_once_with('hashed_password', old_password)

    @patch('src.db.user_details.exec_commit')
    def test_update_password(self, mock_exec_commit):
        hashed_password = 'new_hashed_password'
        username = 'johndoe'
        update_passord(hashed_password, username)
        mock_exec_commit.assert_called_once_with(
            '''UPDATE "user" SET password = %s WHERE username = %s''', (hashed_password, username)
        )

    @patch('src.db.user_details.exec_commit')
    def test_update_user_image_url(self, mock_exec_commit):
        user_id = 'johndoe'
        url = 'http://example.com/image.jpg'
        result = update_user_image_url(user_id, url)
        self.assertEqual(result, "Image URL updated successfully")
        mock_exec_commit.assert_called_once_with(
            '''UPDATE "user" SET profile_pic = %s WHERE username = %s;''', (url, user_id)
        )

    @patch('src.db.user_details.exec_commit')
    def test_update_group_image_url(self, mock_exec_commit):
        group_id = 1
        url = 'http://example.com/image.jpg'
        result = update_group_image_url(group_id, url)
        self.assertEqual(result, "Image URL updated successfully")
        mock_exec_commit.assert_called_once_with(
            '''UPDATE Groups SET profile_picture = %s WHERE GroupID = %s;''', (url, group_id)
        )

    @patch('src.db.user_details.exec_get_all')
    def test_profile_picture(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('http://example.com/profile_pic.jpg',)]
        username = 'johndoe'
        result = profile_picture(username)
        self.assertEqual(result, ('http://example.com/profile_pic.jpg',))
        mock_exec_get_all.assert_called_once_with(
            '''SELECT profile_pic FROM "user" WHERE username = %s;''', (username,)
        )

    @patch('src.db.user_details.exec_get_all')
    def test_group_profile_picture(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('http://example.com/group_pic.jpg',)]
        group_id = 1
        result = group_profile_picture(group_id)
        self.assertEqual(result, ('http://example.com/group_pic.jpg',))
        mock_exec_get_all.assert_called_once_with(
            '''SELECT profile_picture FROM Groups WHERE GroupID = %s''', (group_id,)
        )

    @patch('src.db.user_details.exec_get_all')
    def test_check_friendship_and_get_profile_pic(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('http://example.com/profile_pic.jpg',)]
        user_id = 1
        friend_id = 2
        result = check_friendship_and_get_profile_pic(user_id, friend_id)
        self.assertEqual(result, 'http://example.com/profile_pic.jpg')
        mock_exec_get_all.assert_called_once_with(
            '''
    SELECT u.profile_pic 
    FROM "user" u
    JOIN Friends f ON (u.user_id = f.FriendUserID OR u.user_id = f.UserID)
    WHERE ((f.UserID = %s AND f.FriendUserID = %s) OR (f.UserID = %s AND f.FriendUserID = %s))
      AND f.Status = 'accepted';
    ''', (user_id, friend_id, friend_id, user_id)
        )

    @patch('src.db.user_details.exec_get_all')
    @patch('src.db.user_details.exec_commit')
    def test_delete_account(self, mock_exec_commit, mock_exec_get_all):
        mock_exec_get_all.side_effect = [
            [('1',)],  # User exists
            []  # User does not exist after deletion
        ]
        username = 'johndoe'
        result = delete_account(username)
        self.assertTrue(result)
        mock_exec_get_all.assert_any_call('SELECT 1 FROM "user" WHERE username = %s', (username,))
        mock_exec_commit.assert_called_once_with('DELETE FROM "user" WHERE username = %s', (username,))

if __name__ == '__main__':
    unittest.main()
