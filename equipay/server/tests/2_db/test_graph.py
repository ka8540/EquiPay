import unittest
from unittest.mock import patch
from src.db.graph import get_graph_values  # Adjust the import based on your project structure

class TestGraphFunctions(unittest.TestCase):

    @patch('src.db.graph.exec_get_all')  # Adjust the patch target based on your project structure
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
        mock_exec_get_all.assert_called_once_with(
            '''
    SELECT amount, date FROM Expenses WHERE PayerID = %s
    UNION ALL
    SELECT amount, date FROM GroupExpenses WHERE PayerID = %s;
    ''', (user_id, user_id)
        )

if __name__ == '__main__':
    unittest.main()
