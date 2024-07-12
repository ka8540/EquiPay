from utilities.swen_344_db_utils import exec_get_all

def fetch_user_expenses(user_id):
    sql = '''
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
    return exec_get_all(sql, (user_id, user_id, user_id, user_id))
