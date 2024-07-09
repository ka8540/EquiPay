from utilities.swen_344_db_utils import exec_get_all, exec_get_one

def get_graph_values(user_id):
    query = '''
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
    WHERE d.OwedByUserID = %s;
    '''
    results = exec_get_all(query, (user_id, user_id, user_id))
    print("Combined Graph Values:", results)
    return results


def get_session_key(user_id):
    query = '''SELECT session_key FROM "user" WHERE user_id = %s;'''
    result = exec_get_one(query, (user_id,))
    print("Session_key:",result)
    return result


