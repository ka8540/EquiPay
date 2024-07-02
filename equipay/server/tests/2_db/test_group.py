import unittest
from unittest.mock import patch
from src.db.group import (
    get_groups_by_user_id, create_group, add_group_member, get_group_members_by_group_id,
    get_groups_by_group_id, split_group_expense, create_group_expense, calculate_group_amount_owed,
    get_group_debts, get_group_member_ids, delete_group_debt, get_group_expenses
)  # Adjust the import based on your project structure

class TestGroupFunctions(unittest.TestCase):

    @patch('src.db.group.exec_get_all')
    def test_get_groups_by_user_id_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [(1, 'Group1', True), (2, 'Group2', False)]
        user_id = 1
        result = get_groups_by_user_id(user_id)
        expected_result = [{'group_id': 1, 'group_name': 'Group1', 'is_admin': True},
                           {'group_id': 2, 'group_name': 'Group2', 'is_admin': False}]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            """
    SELECT g.GroupID, g.GroupName, gm.IsAdmin
    FROM Groups g
    JOIN GroupMembers gm ON g.GroupID = gm.GroupID
    WHERE gm.UserID = %s;
    """, (user_id,)
        )

    @patch('src.db.group.exec_commit')
    @patch('src.db.group.exec_get_one')
    def test_create_group_success(self, mock_exec_get_one, mock_exec_commit):
        mock_exec_get_one.return_value = [1]
        group_name = 'New Group'
        user_id = 1
        profile_picture_url = 'http://example.com/pic.jpg'
        result = create_group(group_name, user_id, profile_picture_url)
        expected_result = [1]
        self.assertEqual(result, expected_result)
        mock_exec_commit.assert_called_once_with(
            """
    INSERT INTO Groups (GroupName, CreatedBy, profile_picture)
    VALUES (%s, %s, %s) RETURNING GroupID;
    """, (group_name, user_id, profile_picture_url)
        )
        mock_exec_get_one.assert_called_once_with(
            '''SELECT GroupID FROM Groups WHERE GroupName = %s;''', (group_name,)
        )

    @patch('src.db.group.exec_commit')
    def test_add_group_member_success(self, mock_exec_commit):
        group_id = 1
        user_id = 2
        is_admin = True
        add_group_member(group_id, user_id, is_admin)
        mock_exec_commit.assert_called_once_with(
            """
    INSERT INTO GroupMembers (GroupID, UserID, IsAdmin)
    VALUES (%s, %s, %s);
    """, (group_id, user_id, is_admin)
        )

    @patch('src.db.group.exec_get_all')
    def test_get_group_members_by_group_id_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [(1, 'User1', True), (2, 'User2', False)]
        group_id = 1
        result = get_group_members_by_group_id(group_id)
        expected_result = [{'user_id': 1, 'first_name': 'User1', 'is_admin': True},
                           {'user_id': 2, 'first_name': 'User2', 'is_admin': False}]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            """
    SELECT u.user_id, u.firstname, gm.IsAdmin
    FROM "user" u
    JOIN GroupMembers gm ON u.user_id = gm.UserID
    WHERE gm.GroupID = %s;
    """, (group_id,)
        )

    @patch('src.db.group.exec_get_all')
    def test_get_groups_by_group_id_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [('Group1',)]
        group_id = 1
        result = get_groups_by_group_id(group_id)
        expected_result = [('Group1',)]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            """
    SELECT GroupName FROM Groups WHERE GroupID = %s;
    """, (group_id,)
        )
        
    @patch('src.db.group.exec_fetch')
    def test_create_group_expense_success(self, mock_exec_fetch):
        mock_exec_fetch.return_value = [1]
        group_id = 1
        payer_id = 1
        amount = 100
        description = 'Test expense'
        result = create_group_expense(group_id, payer_id, amount, description)
        expected_result = 1
        self.assertEqual(result, expected_result)
        mock_exec_fetch.assert_called_once_with(
            """
    INSERT INTO GroupExpenses (GroupID, PayerID, Amount, Description, Date)
    VALUES (%s, %s, %s, %s, NOW()) RETURNING ExpenseID;
    """, (group_id, payer_id, amount, description)
        )

    @patch('src.db.group.exec_get_one')
    def test_calculate_group_amount_owed_success(self, mock_exec_get_one):
        mock_exec_get_one.return_value = [100]
        group_id = 1
        payer_id = 2
        receiver_id = 1
        result = calculate_group_amount_owed(group_id, payer_id, receiver_id)
        expected_result = 100
        self.assertEqual(result, expected_result)
        mock_exec_get_one.assert_called_once_with(
            """
    SELECT COALESCE(SUM(AmountOwed), 0) FROM GroupDebts gd
    JOIN GroupExpenses ge ON gd.ExpenseID = ge.ExpenseID
    WHERE ge.GroupID = %s AND gd.OwedToUserID = %s AND gd.OwedByUserID = %s;
    """, (group_id, payer_id, receiver_id)
        )

    @patch('src.db.group.exec_get_all')
    def test_get_group_debts_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            (1, 2, 'User2', 'User1', 50),
            (2, 1, 'User1', 'User2', 100)
        ]
        group_id = 1
        user_id = 1
        result = get_group_debts(group_id, user_id)
        expected_result = [
            (1, 2, 'User2', 'User1', 50),
            (2, 1, 'User1', 'User2', 100)
        ]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            """
    SELECT 
    gd.OwedByUserID AS creditor_id, 
    gd.OwedToUserID AS debtor_id, 
    u.firstname AS debtor_name, 
    u2.firstname AS creditor_name, 
    SUM(gd.AmountOwed) AS total_owed
    FROM GroupDebts gd
    JOIN GroupExpenses ge ON gd.ExpenseID = ge.ExpenseID
    JOIN "user" u ON gd.OwedByUserID = u.user_id
    JOIN "user" u2 ON gd.OwedToUserID = u2.user_id
    WHERE ge.GroupID = %s AND (gd.OwedByUserID = %s OR gd.OwedToUserID = %s) AND gd.OwedByUserID != gd.OwedToUserID
    GROUP BY gd.OwedByUserID, gd.OwedToUserID, u.firstname, u2.firstname;

    """, (group_id, user_id, user_id)
        )

    @patch('src.db.group.exec_get_all')
    def test_get_group_member_ids_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [(1,), (2,)]
        group_id = 1
        result = get_group_member_ids(group_id)
        expected_result = [1, 2]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            """
    SELECT UserID FROM GroupMembers WHERE GroupID = %s;
    """, (group_id,)
        )

    @patch('src.db.group.exec_commit')
    def test_delete_group_debt_success(self, mock_exec_commit):
        user_id = 1
        friend_id = 2
        amount_owed = 50
        group_id = 1
        result = delete_group_debt(user_id, friend_id, amount_owed, group_id)
        self.assertTrue(result)
        mock_exec_commit.assert_called_once_with(
            '''
    DELETE FROM GroupDebts
    WHERE ((OwedToUserID = %s AND OwedByUserID = %s AND AmountOwed = %s AND ExpenseID IN 
           (SELECT ExpenseID FROM GroupExpenses WHERE GroupID = %s))
           OR (OwedToUserID = %s AND OwedByUserID = %s AND AmountOwed = %s AND ExpenseID IN 
           (SELECT ExpenseID FROM GroupExpenses WHERE GroupID = %s)));
    ''', (user_id, friend_id, amount_owed, group_id, friend_id, user_id, amount_owed, group_id)
        )

    @patch('src.db.group.exec_get_all')
    def test_get_group_expenses_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            (1, 'Expense1', 100, 'User1', '2024-01-01', 50),
            (2, 'Expense2', 200, 'User2', '2024-01-02', 100)
        ]
        user_id = 1
        group_id = 1
        result = get_group_expenses(user_id, group_id)
        expected_result = [
            (1, 'Expense1', 100, 'User1', '2024-01-01', 50),
            (2, 'Expense2', 200, 'User2', '2024-01-02', 100)
        ]
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with(
            """
    SELECT 
        ge.ExpenseID,
        ge.Description,
        ge.Amount AS TotalAmount,
        u.firstname AS PayerName,
        ge.Date AS ExpenseDate,
        COALESCE(SUM(CASE 
            WHEN gd.OwedByUserID = %s AND gd.OwedToUserID != %s THEN -gd.AmountOwed
            WHEN gd.OwedToUserID = %s AND gd.OwedByUserID != %s THEN gd.AmountOwed
            ELSE 0
        END), 0) AS LentOrBorrowedAmount
    FROM 
        GroupExpenses ge
    JOIN 
        "user" u ON ge.PayerID = u.user_id
    LEFT JOIN 
        GroupDebts gd ON ge.ExpenseID = gd.ExpenseID
    WHERE 
        ge.GroupID = %s
    GROUP BY
        ge.ExpenseID, ge.Description, ge.Amount, u.firstname, ge.Date;
    """, (user_id, user_id, user_id, user_id, group_id)
        )

if __name__ == '__main__':
    unittest.main()
