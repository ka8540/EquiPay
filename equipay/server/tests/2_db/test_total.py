import unittest
from unittest.mock import patch, MagicMock
from src.db.total import calculate_individual_total_owed, calculate_group_total_owed

class TestTotalFunctions(unittest.TestCase):

    @patch('src.db.total.exec_get_one')
    def test_calculate_individual_total_owed(self, mock_exec_get_one):
        # Mock exec_get_one to return a sum
        mock_exec_get_one.return_value = (150.0,)
        
        user_id = 1

        # Call the function
        result = calculate_individual_total_owed(user_id)

        # Assertions
        self.assertEqual(result, 150.0)
        mock_exec_get_one.assert_called_once_with(
            """
    SELECT 
    SUM(
        CASE 
            WHEN d.OwedToUserID = %s AND d.OwedByUserID != %s THEN d.AmountOwed
            WHEN d.OwedByUserID = %s AND d.OwedToUserID != %s THEN -d.AmountOwed
            ELSE 0
        END
    ) AS NetAmountCreditedToUser
    FROM 
        Debts d
    JOIN 
        Expenses e ON d.ExpenseID = e.ExpenseID
    WHERE 
        d.OwedToUserID = %s OR d.OwedByUserID = %s;
    """,
            (user_id, user_id, user_id, user_id, user_id, user_id)
        )

    @patch('src.db.total.exec_get_one')
    def test_calculate_group_total_owed(self, mock_exec_get_one):
        # Mock exec_get_one to return a sum
        mock_exec_get_one.return_value = (200.0,)
        
        user_id = 1

        # Call the function
        result = calculate_group_total_owed(user_id)

        # Assertions
        self.assertEqual(result, 200.0)
        mock_exec_get_one.assert_called_once_with(
            """
    SELECT 
        SUM(
            CASE 
                WHEN gd.OwedToUserID = %s AND gd.OwedByUserID != %s THEN gd.AmountOwed
                WHEN gd.OwedByUserID = %s AND gd.OwedToUserID != %s THEN -gd.AmountOwed
                ELSE 0
            END
        ) AS NetAmountCreditedToUser
    FROM 
        GroupDebts gd
    JOIN 
        GroupExpenses ge ON gd.ExpenseID = ge.ExpenseID
    WHERE 
        ge.GroupID IN (SELECT GroupID FROM GroupMembers WHERE UserID = %s)
        AND (gd.OwedToUserID = %s OR gd.OwedByUserID = %s);
    """,
            (user_id, user_id, user_id, user_id, user_id, user_id, user_id)
        )

if __name__ == '__main__':
    unittest.main()
