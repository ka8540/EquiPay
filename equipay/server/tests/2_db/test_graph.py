import unittest
from unittest.mock import patch
from src.db.graph import get_graph_values, get_session_key  # Adjust the import based on your project structure

class TestGraphFunctions(unittest.TestCase):

    @patch('src.db.graph.exec_get_all')
    def test_get_graph_values_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            (100.0, '2024-01-01'),
            (200.0, '2024-01-02')
        ]
    
        user_id = 1
        result = get_graph_values(user_id)
    
        expected_result = [
            (100.0, '2024-01-01'),
            (200.0, '2024-01-02')
        ]
        self.assertEqual(result, expected_result)
    
        # Define the expected SQL query, normalizing whitespaces comprehensively
        expected_query = '''
        SELECT amount AS Amount, date AS Date
        FROM Expenses
        WHERE PayerID = %s
    
        UNION ALL
    
        SELECT amount AS Amount, date AS Date
        FROM GroupExpenses
        WHERE PayerID = %s
    
        UNION ALL
    
        SELECT
            d.AmountOwed AS Amount,
            e.Date AS Date
        FROM Debts d
        JOIN Expenses e ON d.ExpenseID = e.ExpenseID
        WHERE d.OwedByUserID = %s AND d.OwedToUserID <> d.OwedByUserID;
        '''
        expected_query = ' '.join(expected_query.strip().split())
    
        # Verify that exec_get_all was called correctly
        actual_query = ' '.join(mock_exec_get_all.call_args[0][0].strip().split())
        self.assertEqual(actual_query, expected_query)
        self.assertEqual(mock_exec_get_all.call_args[0][1], (user_id, user_id, user_id))

    @patch('src.db.graph.exec_get_one')
    def test_get_session_key_success(self, mock_exec_get_one):
        mock_exec_get_one.return_value = ('abcdef123456',)

        user_id = 1
        result = get_session_key(user_id)

        expected_result = ('abcdef123456',)
        
        self.assertEqual(result, expected_result)

        expected_query = 'SELECT session_key FROM "user" WHERE user_id = %s;'
        expected_query = ' '.join(expected_query.strip().split())

        mock_exec_get_one.assert_called_once_with(expected_query, (user_id,))

if __name__ == '__main__':
    unittest.main()
