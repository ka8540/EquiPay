import unittest
from unittest.mock import patch
from src.utilities.swen_344_db_utils import exec_get_one, exec_get_all, exec_commit
from src.db.amoutowed import calculate_amount_owed, get_user_id, get_user_debts, get_debts_by_friend, delete_debt

class TestAmountOwedFunctions(unittest.TestCase):

    @patch('src.db.amoutowed.exec_get_one')
    def test_calculate_amount_owed_success(self, mock_exec_get_one):
        mock_exec_get_one.return_value = [100.0]
        
        payer_id = 1
        receiver_id = 2
        amount_owed = calculate_amount_owed(payer_id, receiver_id)

        self.assertEqual(amount_owed, 100.0)
        mock_exec_get_one.assert_called_once_with("""
    SELECT COALESCE(SUM(AmountOwed), 0) FROM Debts
    WHERE OwedToUserID = %s AND OwedByUserID = %s;
    """, (receiver_id, payer_id))

    @patch('src.db.amoutowed.exec_get_one')
    def test_get_user_id_success(self, mock_exec_get_one):
        mock_exec_get_one.return_value = [1]
        
        username = 'testuser'
        user_id = get_user_id(username)

        self.assertEqual(user_id, 1)
        mock_exec_get_one.assert_called_once_with('''SELECT user_id FROM "user" WHERE username = %s;''', (username,))

    @patch('src.db.amoutowed.exec_get_all')
    def test_get_user_debts_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            (2, 'Friend1', 50.0),
            (3, 'Friend2', -25.0)
        ]
        
        user_id = 1
        debts = get_user_debts(user_id)

        expected_debts = [
            (2, 'Friend1', 50.0),
            (3, 'Friend2', -25.0)
        ]
        self.assertEqual(debts, expected_debts)
        mock_exec_get_all.assert_called_once_with("""
    SELECT 
        CASE 
            WHEN d.OwedToUserID = %s THEN d.OwedByUserID  -- If current user is the creditor, get debtor's ID
            ELSE d.OwedToUserID  -- If current user is the debtor, get creditor's ID
        END AS friend_id,
        CASE 
            WHEN d.OwedToUserID = %s THEN u.firstname  -- If current user is the creditor, get debtor's name
            ELSE u.firstname  -- If current user is the debtor, get creditor's name
        END AS friend_name,
        SUM(CASE 
            WHEN d.OwedToUserID = %s THEN d.AmountOwed  -- Sum amounts owed to user by friends
            ELSE -d.AmountOwed  -- Sum amounts user owes to friends
        END) AS net_amount
    FROM Debts d
    JOIN "user" u ON u.user_id = CASE WHEN d.OwedToUserID = %s THEN d.OwedByUserID ELSE d.OwedToUserID END
    WHERE %s IN (d.OwedToUserID, d.OwedByUserID) AND d.OwedToUserID != d.OwedByUserID
    GROUP BY friend_id, friend_name
    """, (user_id, user_id, user_id, user_id, user_id))

    @patch('src.db.amoutowed.exec_get_all')
    def test_get_debts_by_friend_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            (100.0, 'Dinner', '2024-07-01'),
            (50.0, 'Movie', '2024-07-02')
        ]
        
        user_id = 1
        friend_id = 2
        debts = get_debts_by_friend(user_id, friend_id)

        expected_debts = [
            {'amount_owed': 100.0, 'description': 'Dinner', 'date': '2024-07-01'},
            {'amount_owed': 50.0, 'description': 'Movie', 'date': '2024-07-02'}
        ]
        self.assertEqual(debts, expected_debts)
        mock_exec_get_all.assert_called_once_with("""
    SELECT d.AmountOwed, e.Description, e.Date
    FROM Debts d
    JOIN Expenses e ON d.ExpenseID = e.ExpenseID
    WHERE (d.OwedToUserID = %s AND d.OwedByUserID = %s)
    or (d.OwedToUserID = %s AND d.OwedByUserID = %s);
    """, (user_id, friend_id, friend_id, user_id))

    @patch('src.db.amoutowed.exec_commit')
    def test_delete_debt_success(self, mock_exec_commit):
        mock_exec_commit.return_value = None
        
        user_id = 1
        friend_id = 2
        result = delete_debt(user_id, friend_id)

        self.assertTrue(result)
        mock_exec_commit.assert_called_once_with("""
    DELETE FROM Debts
    WHERE (OwedToUserID = %s AND OwedByUserID = %s);
    """, (user_id, friend_id))

    @patch('src.db.amoutowed.exec_commit', side_effect=Exception("Deletion error"))
    def test_delete_debt_failure(self, mock_exec_commit):
        user_id = 1
        friend_id = 2
        result = delete_debt(user_id, friend_id)

        self.assertFalse(result)
        mock_exec_commit.assert_called_once_with("""
    DELETE FROM Debts
    WHERE (OwedToUserID = %s AND OwedByUserID = %s);
    """, (user_id, friend_id))

if __name__ == '__main__':
    unittest.main()
