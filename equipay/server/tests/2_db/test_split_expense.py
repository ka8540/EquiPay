import unittest
from unittest.mock import patch, MagicMock
from src.db.split_expense import split_expense_

class TestSplitExpense(unittest.TestCase):

    @patch('src.db.split_expense.exec_commit')
    @patch('src.db.split_expense.exec_get_one')
    @patch('src.db.split_expense.exec_fetch')
    def test_split_expense_success(self, mock_exec_fetch, mock_exec_get_one, mock_exec_commit):
        # Mock exec_get_one to return a user ID
        mock_exec_get_one.return_value = (1,)
        
        # Mock exec_fetch to return an expense ID
        mock_exec_fetch.return_value = (100,)

        # Define input parameters
        usercreds = 'testuser'
        amount = 100.0
        friend_ids = [2, 3]
        include_self = True
        description = 'Dinner'

        # Call the function
        result = split_expense_(usercreds, amount, friend_ids, include_self, description)

        # Assertions
        self.assertTrue(result)
        mock_exec_get_one.assert_called_once_with('''SELECT user_id FROM "user" WHERE username = %s;''', (usercreds,))
        mock_exec_fetch.assert_called_once_with(
            '\n    INSERT INTO Expenses (PayerID, Amount, Description, Date)\n    VALUES (%s, %s, %s, NOW()) RETURNING ExpenseID;\n    ',
            (1, amount, description)
        )
        self.assertEqual(mock_exec_commit.call_count, 3)  # 2 friends + 1 self
        mock_exec_commit.assert_any_call(
            "INSERT INTO Debts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed) VALUES (%s, %s, %s, %s)",
            (100, 1, 2, 33.333333333333336)
        )
        mock_exec_commit.assert_any_call(
            "INSERT INTO Debts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed) VALUES (%s, %s, %s, %s)",
            (100, 1, 3, 33.333333333333336)
        )
        mock_exec_commit.assert_any_call(
            "INSERT INTO Debts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed) VALUES (%s, %s, %s, %s)",
            (100, 1, 1, 33.333333333333336)
        )

if __name__ == '__main__':
    unittest.main()
