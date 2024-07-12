import unittest
from unittest.mock import patch
from src.db.forecast import fetch_user_expenses  # Update this to your actual module name

class FetchUserExpensesTestCase(unittest.TestCase):

    @patch('src.db.forecast.exec_get_all')  # Update this to the correct import path
    def test_fetch_user_expenses(self, mock_exec_get_all):
        # Mock return value for exec_get_all
        mock_exec_get_all.return_value = [
            {'Amount': 100.00, 'Date': '2024-05-01'},
            {'Amount': 150.00, 'Date': '2024-06-01'},
            {'Amount': 50.00, 'Date': '2024-05-10'},
            {'Amount': 75.00, 'Date': '2024-06-10'}
        ]

        user_id = 1
        result = fetch_user_expenses(user_id)

        expected_sql = '''
    SELECT Amount, Date FROM Expenses WHERE PayerID = %s
    UNION ALL
    SELECT Amount, Date FROM GroupExpenses WHERE PayerID = %s
    UNION ALL
    SELECT AmountOwed as Amount, E.Date FROM Debts D
    JOIN Expenses E ON D.ExpenseID = E.ExpenseID
    WHERE D.OwedByUserID = %s
    UNION ALL
    SELECT AmountOwed as Amount, GE.Date FROM GroupDebts GD
    JOIN GroupExpenses GE ON GD.ExpenseID = GE.ExpenseID
    WHERE GD.OwedByUserID = %s
    '''

        # Assert exec_get_all was called with the correct SQL and parameters
        mock_exec_get_all.assert_called_once_with(expected_sql, (user_id, user_id, user_id, user_id))

        # Assert the result matches the mock return value
        self.assertEqual(result, mock_exec_get_all.return_value)

if __name__ == '__main__':
    unittest.main()
